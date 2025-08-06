import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from dotenv import load_dotenv
from flask import Flask, request, json

from src.states import RegistrationStates
from src.constants import BROADCAST_MESSAGE
from src.services.admin_service import AdminService
from src.services.sheet_service import SheetService
from handlers.start import start
from handlers.registration import (
    registration_name, registration_father_name, registration_phone, registration_education,
    registration_other_education, registration_department, registration_finish,
    registration_confirmation,
    back_to_phone,
    back_to_department,
    cancel
)

from handlers.admin import admin_view, add_admin_command, remove_admin_command, send_admin_welcome
from handlers.broadcast import broadcast, send_broadcast, cancel_broadcast
from handlers.error import error_handler
from config.config import BOT_TOKEN, GOOGLE_SHEETS_CREDENTIALS, SHEET_ID, INITIAL_ADMIN_ID, WEBHOOK_URL

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

def main():
    """Main function to run the Telegram bot."""
    # Load environment variables
    load_dotenv()

    # Initialize services
    admin_service = AdminService(INITIAL_ADMIN_ID)
    admin_service.load_admins()
    sheet_service = SheetService(GOOGLE_SHEETS_CREDENTIALS, SHEET_ID)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add services to bot_data
    application.bot_data["admin_service"] = admin_service
    application.bot_data["sheet_service"] = sheet_service

    # Conversation handler for registration
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler("register", registration_name), CallbackQueryHandler(pattern="register", callback=registration_name)],
        states={
            RegistrationStates.REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_father_name)],
            RegistrationStates.REGISTER_FATHER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_phone)],
            RegistrationStates.REGISTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_education)],
            RegistrationStates.REGISTER_EDUCATION: [
                CallbackQueryHandler(registration_other_education, pattern='^(?!back_to_phone$).*$'),
                CallbackQueryHandler(back_to_phone, pattern='^back_to_phone$')
            ],
            RegistrationStates.REGISTER_OTHER_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_department)],
            RegistrationStates.REGISTER_DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_confirmation)],
            RegistrationStates.REGISTER_CONFIRMATION: [
                CallbackQueryHandler(registration_finish, pattern='^(?!back_to_department$).*$'),
                CallbackQueryHandler(back_to_department, pattern='^back_to_department$')
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Conversation handler for broadcast
    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast)],
        states={
            BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_broadcast)],
        },
        fallbacks=[CommandHandler("cancel", cancel_broadcast)],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin_welcome", send_admin_welcome))
    application.add_handler(registration_handler)
    application.add_handler(broadcast_handler)
    application.add_handler(CommandHandler("admin_view", admin_view))
    
    application.add_handler(CommandHandler("add_admin", add_admin_command))
    application.add_handler(CommandHandler("remove_admin", remove_admin_command))
    
    application.add_error_handler(error_handler)

    # Set up webhook
    @app.route('/webhook', methods=['POST'])
    async def webhook_handler():
        """Set up webhook for the bot."""
        if request.method == "POST":
            update = Update.de_json(request.get_json(force=True), application.bot)
            await application.process_update(update)
        return "ok"

    # Run the bot
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", "8443")),
        url_path="/webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
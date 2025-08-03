
import os
import logging
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

from bot.constants import (
    REGISTER_NAME, REGISTER_FATHER_NAME, REGISTER_PHONE, REGISTER_EDUCATION,
    REGISTER_OTHER_EDUCATION, REGISTER_DEPARTMENT, REGISTER_USERNAME, REGISTER_ROUND,
    BROADCAST_MESSAGE
)
from bot.services.admin_service import AdminService
from bot.services.sheet_service import SheetService
from handlers.start import start
from handlers.registration import (
    registration_name, registration_father_name, registration_phone, registration_education,
    registration_other_education, registration_department, registration_username, registration_round,
    cancel
)
from handlers.payment import payment_upload, payment_approve
from handlers.admin import admin_view, add_admin_command, remove_admin_command, send_admin_welcome
from handlers.broadcast import broadcast, send_broadcast, cancel_broadcast
from handlers.error import error_handler
from config.config import BOT_TOKEN, GOOGLE_SHEETS_CREDENTIALS, SHEET_ID

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the Telegram bot."""
    # Initialize services
    admin_service = AdminService()
    await admin_service.load_admins()
    sheet_service = SheetService(GOOGLE_SHEETS_CREDENTIALS, SHEET_ID)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add services to bot_data
    application.bot_data["admin_service"] = admin_service
    application.bot_data["sheet_service"] = sheet_service

    # Conversation handler for registration
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler("register", registration_name)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_father_name)],
            REGISTER_FATHER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_phone)],
            REGISTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_education)],
            REGISTER_EDUCATION: [
                MessageHandler(filters.Regex("^(ወደ 12|9ኛ ክፍል|10ኛ ክፍል|11ኛ ክፍል|Other)$|"), registration_other_education),
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration_education),
            ],
            REGISTER_OTHER_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_department)],
            REGISTER_DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_username)],
            REGISTER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_round)],
            REGISTER_ROUND: [MessageHandler(filters.Regex("^(Round 1|Round 2)"), registration_round)],
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
    application.add_handler(CommandHandler("approve", payment_approve))
    application.add_handler(CommandHandler("add_admin", add_admin_command))
    application.add_handler(CommandHandler("remove_admin", remove_admin_command))
    application.add_handler(MessageHandler(filters.PHOTO, payment_upload))
    application.add_error_handler(error_handler)

    # Start the bot
    await application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

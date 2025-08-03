
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.constants import BROADCAST_MESSAGE

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start broadcast message process."""
    admin_service = context.bot_data["admin_service"]
    if not admin_service.is_admin(update.message.from_user.id):
        await update.message.reply_text("Unauthorized.")
        return ConversationHandler.END

    await update.message.reply_text("Enter the message to broadcast to all approved users:")
    return BROADCAST_MESSAGE

async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send broadcast message to all approved users."""
    sheet_service = context.bot_data["sheet_service"]
    message = update.message.text
    approved_users = sheet_service.get_approved_users()

    for username in approved_users:
        try:
            await context.bot.send_message(chat_id=username, text=message)
        except Exception as e:
            await update.message.reply_text(f"Failed to send to {username}: {str(e)}")

    await update.message.reply_text("Broadcast sent to all approved users.")
    return ConversationHandler.END

async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel broadcast."""
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END

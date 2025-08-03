from telegram import Update
from telegram.ext import ContextTypes
from config.config import WELCOME_MESSAGE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(WELCOME_MESSAGE)
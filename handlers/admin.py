from telegram import Update
from telegram.ext import ContextTypes
from utils.sheets import get_registrations
from config.config import ADMIN_IDS

async def admin_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to view registrations."""
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("Unauthorized.")
        return
    round_filter = context.args[0] if context.args else None
    registrations = get_registrations(round_filter)
    if not registrations:
        await update.message.reply_text("No registrations found.")
        return
    message = f"Registrations ({'All' if not round_filter else round_filter}):\n"
    for r in registrations:
        message += (f"Name: {r['Name']}, Phone: {r['Phone Number']}, "
                   f"Round: {r['Round']}, Payment: {r['Payment Status']}, Membership: {r['Membership Status']}\n")
    await update.message.reply_text(message)
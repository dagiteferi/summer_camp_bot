from telegram import Update
from telegram.ext import ContextTypes
from utils.sheets import save_registration, update_payment_and_membership_status, get_registrations
from utils.batch import generate_batch_number
from utils.admin_utils import is_admin, get_admins
from config.config import SUCCESS_MESSAGE, PENDING_MESSAGE

async def payment_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment screenshot upload."""
    if update.message.photo:
        registration = context.user_data.get("registration", {})
        if not registration:
            await update.message.reply_text("Please register first using /register.")
            return
        for admin_id in get_admins():
            await context.bot.send_photo(
                admin_id,
                update.message.photo[-1].file_id,
                caption=f"New payment from {registration['username']} for {registration['round']}. Verify membership."
            )
        await update.message.reply_text("Payment screenshot received. Await admin approval for payment and membership.")
    else:
        await update.message.reply_text("Please upload a payment screenshot or photo.")

async def payment_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to approve payment and membership."""
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("Unauthorized.")
        return
    try:
        telegram_id = context.args[0]
        registration = next((r for r in get_registrations() if r["Telegram Username"] == telegram_id), None)
        if not registration:
            await update.message.reply_text("User not found.")
            return
        batch_number = generate_batch_number()
        update_payment_and_membership_status(telegram_id, "Approved", "Approved", batch_number)
        await context.bot.send_message(
            telegram_id,
            SUCCESS_MESSAGE.format(batch_number=batch_number)
        )
        await update.message.reply_text(f"Payment and membership approved for {telegram_id}. Batch: {batch_number}")
    except IndexError:
        await update.message.reply_text("Usage: /approve @username")

from telegram import Update
from telegram.ext import ContextTypes
from utils.batch import generate_batch_number
from config.config import SUCCESS_MESSAGE

async def payment_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment screenshot upload."""
    admin_service = context.bot_data["admin_service"]
    registration = context.user_data.get("registration", {})

    if not registration:
        await update.message.reply_text("Please register first using /register.")
        return

    if update.message.photo:
        for admin_id in admin_service.get_admins():
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
    admin_service = context.bot_data["admin_service"]
    if not admin_service.is_admin(update.message.from_user.id):
        await update.message.reply_text("Unauthorized.")
        return

    sheet_service = context.bot_data["sheet_service"]
    try:
        telegram_id = context.args[0]
        batch_number = generate_batch_number()
        if sheet_service.update_payment_and_membership_status(telegram_id, "Approved", "Approved", batch_number):
            await context.bot.send_message(
                telegram_id,
                SUCCESS_MESSAGE.format(batch_number=batch_number)
            )
            await update.message.reply_text(f"Payment and membership approved for {telegram_id}. Batch: {batch_number}")
        else:
            await update.message.reply_text("User not found.")
    except IndexError:
        await update.message.reply_text("Usage: /approve @username")

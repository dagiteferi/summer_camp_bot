
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from utils.validators import validate_name, validate_phone
from config.config import PAYMENT_INSTRUCTIONS, PENDING_MESSAGE, ACTIVE_ROUND
from src.constants import (
    REGISTER_NAME, REGISTER_FATHER_NAME, REGISTER_PHONE, REGISTER_EDUCATION,
    REGISTER_OTHER_EDUCATION, REGISTER_DEPARTMENT, REGISTER_CONFIRMATION
)

async def registration_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start registration and ask for name."""
    context.user_data["registration"] = {}
    await update.message.reply_text("Please enter your name / ስምዎን ያስገቡ")
    return REGISTER_NAME

async def registration_father_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for father's name."""
    name = update.message.text
    if not validate_name(name):
        await update.message.reply_text("Invalid name. Use letters only. / ስም ተገቢ አይደለም። ፊደሎችን ብቻ ይጠቀሙ።")
        return REGISTER_NAME
    context.user_data["registration"]["name"] = name
    await update.message.reply_text("Please enter your father's name / የአባትዎን ስም ያስገቡ")
    return REGISTER_FATHER_NAME

async def registration_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for phone number."""
    father_name = update.message.text
    if not validate_name(father_name):
        await update.message.reply_text("Invalid father's name. Use letters only. / የአባት ስም ተገቢ አይደለም።")
        return REGISTER_FATHER_NAME
    context.user_data["registration"]["father_name"] = father_name
    await update.message.reply_text("Please enter your phone number / ስልክ ቁጥርዎን ያስገቡ")
    return REGISTER_PHONE

async def registration_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for education level."""
    phone = update.message.text
    if not validate_phone(phone):
        await update.message.reply_text("Invalid phone number. Use +251 or 0 followed by 9 digits. / ስልክ ቁጥር ተገቢ አይደለም።")
        return REGISTER_PHONE
    context.user_data["registration"]["phone"] = phone
    keyboard = [
        [InlineKeyboardButton("ወደ 12", callback_data="ወደ 12"), InlineKeyboardButton("9ኛ ክፍል", callback_data="9ኛ ክፍል")],
        [InlineKeyboardButton("10ኛ ክፍል", callback_data="10ኛ ክፍል"), InlineKeyboardButton("11ኛ ክፍል", callback_data="11ኛ ክፍል")],
        [InlineKeyboardButton("Other", callback_data="Other")]
    ]
    await update.message.reply_text(
        "Select your education level / የትምህርት ሁኔታዎን ይምረጡ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return REGISTER_EDUCATION

async def registration_other_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle education level selection."""
    query = update.callback_query
    await query.answer()
    education = query.data
    if education == "Other":
        await query.edit_message_text("Please specify your education level / የትምህርት ሁኔታዎን ይግለጹ")
        return REGISTER_OTHER_EDUCATION
    context.user_data["registration"]["education"] = education
    await query.edit_message_text("Enter your serving department / የሚያገለግሉበት ሄበርት ያስገቡ")
    return REGISTER_DEPARTMENT

async def registration_department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves custom education and asks for serving department."""
    if "education" not in context.user_data["registration"]:
        context.user_data["registration"]["education"] = update.message.text
    await update.message.reply_text("Enter your serving department / የሚያገለግሉበት ሄበርት ያስገቡ")
    return REGISTER_DEPARTMENT

async def registration_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for confirmation of the provided information."""
    context.user_data["registration"]["department"] = update.message.text
    reg_data = context.user_data["registration"]
    summary = f"""Please confirm your details:

Name: {reg_data['name']}
Father's Name: {reg_data['father_name']}
Phone: {reg_data['phone']}
Education: {reg_data['education']}
Department: {reg_data['department']}"""
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data="confirm"), InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    await update.message.reply_text(summary, reply_markup=InlineKeyboardMarkup(keyboard))
    return REGISTER_CONFIRMATION

async def registration_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves department and finalizes registration."""
    query = update.callback_query
    await query.answer()
    if query.data == "confirm":
        context.user_data["registration"]["user_id"] = update.callback_query.from_user.id
        sheet_service = context.bot_data["sheet_service"]
        context.user_data["registration"]["round"] = ACTIVE_ROUND
        sheet_service.save_registration(context.user_data["registration"])
        await query.edit_message_text("Registration successful!")
        try:
            await context.bot.send_message(
                chat_id=update.callback_query.from_user.id,
                text=PENDING_MESSAGE
            )
            await context.bot.send_message(
                chat_id=update.callback_query.from_user.id,
                text=PAYMENT_INSTRUCTIONS
            )
        except Exception:
            await query.message.reply_text(
                f"{PENDING_MESSAGE}\n\n{PAYMENT_INSTRUCTIONS}\n\nTo receive future messages, please start a private chat with me."
            )
    else:
        await query.edit_message_text("Registration cancelled. / ምዝገባ ተሰрዟል።")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the registration process."""
    await update.message.reply_text("Registration cancelled. / ምዝገባ ተሰርዟል።")
    return ConversationHandler.END


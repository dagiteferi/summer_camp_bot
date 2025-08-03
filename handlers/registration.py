
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from utils.validators import validate_name, validate_phone
from config.config import PAYMENT_INSTRUCTIONS, PENDING_MESSAGE
from src.constants import (
    REGISTER_NAME, REGISTER_FATHER_NAME, REGISTER_PHONE, REGISTER_EDUCATION,
    REGISTER_OTHER_EDUCATION, REGISTER_DEPARTMENT, REGISTER_USERNAME, REGISTER_ROUND
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
    keyboard = [["ወደ 12", "9ኛ ክፍል"], ["10ኛ ክፍል", "11ኛ ክፍል"], ["Other"]]
    await update.message.reply_text(
        "Select your education level / የትምህርት ሁኔታዎን ይምረጡ",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return REGISTER_EDUCATION

async def registration_other_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle education level selection."""
    education = update.message.text
    if education == "Other":
        await update.message.reply_text("Please specify your education level / የትምህርት ሁኔታዎን ይግለጹ")
        return REGISTER_OTHER_EDUCATION
    context.user_data["registration"]["education"] = education
    await update.message.reply_text("Enter your serving department / የሚያገለግሉበት ሄበርት ያስገቡ",
                                   reply_markup=ReplyKeyboardRemove())
    return REGISTER_DEPARTMENT

async def registration_department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves custom education and asks for serving department."""
    if "education" not in context.user_data["registration"]:
        context.user_data["registration"]["education"] = update.message.text
    await update.message.reply_text("Enter your serving department / የሚያገለግሉበት ሄበርት ያስገቡ",
                                   reply_markup=ReplyKeyboardRemove())
    return REGISTER_DEPARTMENT

async def registration_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves department and asks for username if not auto-detected."""
    context.user_data["registration"]["department"] = update.message.text
    username = update.message.from_user.username or ""
    if username:
        context.user_data["registration"]["username"] = username
        keyboard = [["Round 1 (Grades 9–12)", "Round 2 (Grade 12+)"]]
        await update.message.reply_text(
            "Select camp round / የካምፕ ዙር ይምረጡ",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
        return REGISTER_ROUND
    await update.message.reply_text("Enter your Telegram username / የቴሌግራም ተጠቃሚ ስምዎን ያስገቡ")
    return REGISTER_USERNAME

async def registration_round(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles username (if provided) and round selection, then finalizes registration."""
    # If username was not automatically detected, it's provided in this step.
    if "username" not in context.user_data["registration"]:
        username = update.message.text
        if not username.startswith("@"):
            username = f"@{username}"
        context.user_data["registration"]["username"] = username
        keyboard = [["Round 1 (Grades 9–12)", "Round 2 (Grade 12+)"]]
        await update.message.reply_text(
            "Select camp round / የካምፕ ዙር ይምረጡ",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
        return REGISTER_ROUND

    # Handle round selection
    sheet_service = context.bot_data["sheet_service"]
    context.user_data["registration"]["round"] = update.message.text.split(" ")[0]
    sheet_service.save_registration(context.user_data["registration"])
    await context.bot.send_message(
        chat_id=update.message.from_user.id,
        text=PENDING_MESSAGE
    )
    await update.message.reply_text(PAYMENT_INSTRUCTIONS, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the registration process."""
    await update.message.reply_text("Registration cancelled. / ምዝገባ ተሰርዟል።")
    return ConversationHandler.END

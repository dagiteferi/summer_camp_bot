from telegram import Update
from telegram.ext import ContextTypes
from utils.sheets import get_registrations
from utils.admin_utils import is_admin, add_admin, remove_admin, get_admins

async def admin_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to view registrations."""
    if not is_admin(update.message.from_user.id):
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

async def add_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to add a new admin."""
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("Unauthorized.")
        return
    try:
        new_admin_id = int(context.args[0])
        if add_admin(new_admin_id):
            await update.message.reply_text(f"Admin {new_admin_id} added successfully.")
            # Notify other admins
            for admin_id in get_admins():
                if admin_id != update.message.from_user.id:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=f"A new admin with ID {new_admin_id} has been added by {update.message.from_user.id}."
                    )
        else:
            await update.message.reply_text(f"Admin {new_admin_id} is already an admin.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /add_admin <user_id>")

async def remove_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to remove an admin."""
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("Unauthorized.")
        return
    try:
        admin_to_remove_id = int(context.args[0])
        if remove_admin(admin_to_remove_id):
            await update.message.reply_text(f"Admin {admin_to_remove_id} removed successfully.")
            # Notify other admins
            for admin_id in get_admins():
                if admin_id != update.message.from_user.id:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=f"Admin with ID {admin_to_remove_id} has been removed by {update.message.from_user.id}."
                    )
        else:
            await update.message.reply_text(f"Admin {admin_to_remove_id} not found.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /remove_admin <user_id>")

async def send_admin_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message to a new admin."""
    user_id = update.message.from_user.id
    if is_admin(user_id) and user_id not in context.bot_data.get("welcomed_admins", []):
        welcome_message = """
        Welcome to the Admin Team! / ወደ አስተዳደር ቡድን እንኳን በደህና መጡ!

        You have been added as an admin for the Summer Camp Registration Bot.
        ለበጋ ካምፕ ምዝገባ ቦት አስተዳዳሪ ሆነው ተጨምረዋል።

        Here are your responsibilities and available commands:
        የእርስዎ ኃላፊነቶች እና ያሉ ትዕዛዞች እነሆ፡-

        - `/admin_view`: View all registrations.
        - `/admin_view [Round 1/Round 2]`: Filter registrations by round.
        - `/approve @username`: Approve a user's payment and membership.
        - `/broadcast`: Send a message to all approved users.
        - `/add_admin <user_id>`: Add a new admin.
        - `/remove_admin <user_id>`: Remove an admin.

        Please use these commands responsibly.
        እባክዎ እነዚህን ትዕዛዞች በኃላፊነት ይጠቀሙ።
        """
        await update.message.reply_text(welcome_message)
        if "welcomed_admins" not in context.bot_data:
            context.bot_data["welcomed_admins"] = []
        context.bot_data["welcomed_admins"].append(user_id)

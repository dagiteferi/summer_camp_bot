import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")  # Path to JSON key file
SHEET_ID = os.getenv("SHEET_ID")  # Google Sheet ID

# Initial Admin ID
INITIAL_ADMIN_ID = os.getenv("INITIAL_ADMIN_ID")

# Active round
ACTIVE_ROUND = "Round 1"

# Bot Messages
WELCOME_MESSAGE = """
Summer Camp Registration / የበጋ ካምፕ ምዝገባ
This summer camp is organized by Adama Gende Gara Full Gospel Church.
ይህ summer camp በአዳማ ገንደ ጋራ ሙሉ ወንጌል ቤተክርስቲያን ተዘጋጅቷል
📌 Round 1: For church members in Grades 9–12.
📌 የመጀመሪያ ዙር፡ ለቤተክርስቲያን አባላት ከ9–12 ክፍል።
📌 Round 2: For church members in Grade 12 and above.
📌 የሁለተኛ ዙር፡ ለቤተክርስቲያን አባላት ከ12ኛ ክፍል በላይ።
Starts Nehase 6 / ነሀሴ 6 ይጀምራል
Follow us:
Telegram: t.me/yourchurch
Instagram: instagram.com/yourchurch
Use /register to start registration.
"""

# Payment Instructions
PAYMENT_INSTRUCTIONS = """To complete your registration, please pay 400 Birr to the following bank account:

[Bank Account Details]

After paying, please send a screenshot of your payment to this chat."""

# Pending Message
PENDING_MESSAGE = """Congratulations! You have successfully registered for the summer camp.

Your registration is now pending payment. You will receive a batch number once your payment is approved."""

# Success Message
SUCCESS_MESSAGE = """
🎉 Registration successful! / ምዝገባዎ ተሳክቷል!
Batch Number: {batch_number}
Prepare for camp starting Nehase 6! Bring comfortable clothes and a Bible.
ካምፑ ነሀሴ 6 ይጀምራል! ምቹ ልብስ እና መጽሐፍ ቅዱስ ይዘው ይምጡ።
"""
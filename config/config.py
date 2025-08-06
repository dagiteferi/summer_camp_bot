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
Summer Camp Registration /  ካምፕ ምዝገባ
This summer camp is organized by Adama Gende Gara Full Gospel Church.
ይህ summer camp በአዳማ ገንደ ጋራ ሙሉ ወንጌል ቤተክርስቲያን ተዘጋጅቷል
📌 Round 1: For church members in Grades 9–12.
📌 የመጀመሪያ ዙር፡ ከ9–12 ክፍል።
📌 Round 2: For church members in Grade 12 and above.
📌 የሁለተኛ ዙር፡  ከ12ኛ ክፍል በላይ።

Follow us:
Telegram: https://t.me/Sacred_Youth
Instagram: https://www.instagram.com/adama_fullgospel_youth__/



"""




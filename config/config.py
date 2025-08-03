import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")  # Path to JSON key file
SHEET_ID = os.getenv("SHEET_ID")  # Google Sheet ID

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
PAYMENT_INSTRUCTIONS = """
Please transfer 400 ETB to [Bank Account Details].
Upload a screenshot or photo of your payment to complete registration.
እባክዎ 400 ብር ወደ [የባንክ መለያ ዝርዝር] ያስተላልፉ።
ምዝገባዎን ለመጨረስ የክፍያ ማረጋገጫ ፎቶ ይስቀሉ።
"""

# Pending Message
PENDING_MESSAGE = """
Your registration is pending approval. You will receive a batch number once your payment and membership are verified.
ምዝገባዎ ማፅደቂያ እስኪያገኝ ድረስ በጥበቃ ላይ ነው። ክፍያዎ እና የአባልነት ማረጋገጫዎ ከተረጋገጠ በኋላ የባች ቁጥር ይደርስዎታል።
"""

# Success Message
SUCCESS_MESSAGE = """
🎉 Registration successful! / ምዝገባዎ ተሳክቷል!
Batch Number: {batch_number}
Prepare for camp starting Nehase 6! Bring comfortable clothes and a Bible.
ካምፑ ነሀሴ 6 ይጀምራል! ምቹ ልብስ እና መጽሐፍ ቅዱስ ይዘው ይምጡ።
"""
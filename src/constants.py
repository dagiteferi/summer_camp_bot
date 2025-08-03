
# Conversation states
(REGISTER_NAME, REGISTER_FATHER_NAME, REGISTER_PHONE, REGISTER_EDUCATION,
 REGISTER_OTHER_EDUCATION, REGISTER_DEPARTMENT, REGISTER_USERNAME, REGISTER_ROUND) = range(8)

BROADCAST_MESSAGE = 0

# Google Sheets columns
COLUMNS = [
    "Name", "Father's Name", "Phone Number", "Education Level", "Department",
    "Telegram User ID", "Round", "Payment Status", "Membership Status",
    "Batch Number", "Timestamp"
]

# Admin file
ADMIN_FILE = "config/admins.json"

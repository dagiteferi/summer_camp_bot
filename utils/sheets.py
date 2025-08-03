import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.config import GOOGLE_SHEETS_CREDENTIALS, SHEET_ID
from datetime import datetime

def init_sheets():
    """Initialize Google Sheets client."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

def save_registration(data):
    """Save registration data to Google Sheets."""
    sheet = init_sheets()
    row = [
        data["name"],
        data["father_name"],
        data["phone"],
        data["education"],
        data["department"],
        data["username"],
        data["round"],
        data["payment_status"],
        data["membership_status"],
        data["batch_number"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    sheet.append_row(row)

def get_registrations(round=None):
    """Retrieve registrations, optionally filtered by round."""
    sheet = init_sheets()
    records = sheet.get_all_records()
    if round:
        return [r for r in records if r["Round"] == round]
    return records

def update_payment_and_membership_status(telegram_id, payment_status, membership_status, batch_number):
    """Update payment and membership status and batch number for a user."""
    sheet = init_sheets()
    records = sheet.get_all_records()
    for i, record in enumerate(records, start=2):
        if record["Telegram Username"] == telegram_id:
            sheet.update_cell(i, 8, payment_status)  # Payment Status column
            sheet.update_cell(i, 9, membership_status)  # Membership Status column
            sheet.update_cell(i, 10, batch_number)  # Batch Number column
            break

def get_approved_users():
    """Get all approved users for broadcasting."""
    sheet = init_sheets()
    records = sheet.get_all_records()
    return [r["Telegram Username"] for r in records if r["Payment Status"] == "Approved" and r["Membership Status"] == "Approved"]

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from src.constants import COLUMNS

class SheetService:
    def __init__(self, credentials_path, sheet_id):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(sheet_id).sheet1
        self._ensure_header()

    def _ensure_header(self):
        """Ensure the sheet has the correct header row."""
        header = self.sheet.row_values(1)
        if header != COLUMNS:
            self.sheet.insert_row(COLUMNS, 1)

    def save_registration(self, data):
        """Save a new registration to the sheet."""
        row = [
            data["name"],
            data["father_name"],
            data["phone"],
            data["education"],
            data["department"],
            data["username"],
            data["round"],
            "Pending",
            "Pending",
            "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheet.append_row(row)

    def get_registrations(self, round_filter=None):
        """Retrieve registrations, optionally filtered by round."""
        records = self.sheet.get_all_records()
        if round_filter:
            return [r for r in records if r["Round"] == round_filter]
        return records

    def update_payment_and_membership_status(self, telegram_id, payment_status, membership_status, batch_number):
        """Update a user's registration status."""
        cell = self.sheet.find(telegram_id)
        if cell:
            self.sheet.update_cell(cell.row, COLUMNS.index("Payment Status") + 1, payment_status)
            self.sheet.update_cell(cell.row, COLUMNS.index("Membership Status") + 1, membership_status)
            self.sheet.update_cell(cell.row, COLUMNS.index("Batch Number") + 1, batch_number)
            return True
        return False

    def get_approved_users(self):
        """Get all approved users."""
        records = self.sheet.get_all_records()
        return [r["Telegram Username"] for r in records if r["Payment Status"] == "Approved" and r["Membership Status"] == "Approved"]


# How to Test the Summer Camp Bot

This document provides instructions for manually testing the functionality of the Summer Camp Registration Bot.

## 1. Prerequisites

- **Python 3.10+**
- **Virtual Environment:** A configured Python virtual environment.
- **Dependencies:** All required packages installed via `pip install -r requirements.txt`.

## 2. Configuration

Before running the bot, you must set up the necessary credentials and configuration in a `.env` file.

1.  **Create the `.env` file** in the root of the project directory.

2.  **Add the following variables:**

    ```
    # Your Telegram bot token from BotFather
    BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

    # The absolute path to your Google Cloud service account JSON file
    GOOGLE_SHEETS_CREDENTIALS="/path/to/your/credentials.json"

    # The ID of the Google Sheet where registrations will be stored
    SHEET_ID="YOUR_GOOGLE_SHEET_ID"
    ```

3.  **Set up `admins.json`:**
    - Create a file named `admins.json` inside the `config` directory.
    - Add your own Telegram User ID to make yourself the first admin. You can get your ID by messaging `@userinfobot` on Telegram.

    ```json
    {
      "admins": [
        123456789
      ]
    }
    ```

## 3. Running the Bot

Activate your virtual environment and run the `main.py` script:

```bash
# Activate your virtual environment (e.g., venv)
source bot/bin/activate

# Run the bot
python main.py
```

The bot should now be running and connected to Telegram.

## 4. Manual Testing Scenarios

Interact with your bot on Telegram to test the following scenarios.

### Scenario 1: New User Registration

1.  **Start the bot:** Send `/start`.
    - **Expected:** The bot replies with the welcome message.
2.  **Begin registration:** Send `/register`.
    - **Expected:** The bot asks for your name.
3.  **Provide valid details:** Complete the entire registration conversation with valid inputs.
    - **Expected:** The bot sends the pending message and payment instructions.
4.  **Check Google Sheet:**
    - **Expected:** A new row appears in your Google Sheet with your registration details and a "Pending" status for payment and membership.

### Scenario 2: Input Validation

1.  **Start registration:** Send `/register`.
2.  **Enter an invalid name:** Use numbers or symbols (e.g., `Test123`).
    - **Expected:** The bot replies with an error message and asks for the name again.
3.  **Enter an invalid phone number:** Use an incorrect format (e.g., `12345`).
    - **Expected:** The bot replies with an error message and asks for the phone number again.

### Scenario 3: Payment and Approval

1.  **Upload a photo:** After registering, send a photo to the bot.
    - **Expected:** The bot confirms receipt and notifies all admins (you) with the photo and user details.
2.  **Approve the payment:** As an admin, use the `/approve` command with the user's Telegram username (e.g., `/approve @testuser`).
    - **Expected:** The user receives a success message with a unique batch number. The admin who issued the command receives a confirmation.
3.  **Check Google Sheet:**
    - **Expected:** The user's row is updated with "Approved" status for payment and membership, and the new batch number is filled in.

### Scenario 4: Admin Commands

1.  **View registrations:** Send `/admin_view`.
    - **Expected:** The bot replies with a list of all current registrations.
2.  **Add a new admin:** Use `/add_admin <user_id>` with the ID of another user.
    - **Expected:** The bot confirms the new admin was added and notifies all other admins.
3.  **Remove an admin:** Use `/remove_admin <user_id>`.
    - **Expected:** The bot confirms the admin was removed and notifies all other admins.

### Scenario 5: Broadcast

1.  **Start a broadcast:** Send `/broadcast`.
    - **Expected:** The bot asks for the message to send.
2.  **Send the message:** Type a message and send it.
    - **Expected:** The bot sends this message to all users with an "Approved" status and confirms the broadcast is complete.

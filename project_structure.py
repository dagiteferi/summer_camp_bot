import os

project_structure = {
    "config": ["config.py"],
    "handlers": ["start.py", "registration.py", "payment.py", "admin.py", "error.py"],
    "utils": ["sheets.py", "validators.py", "batch.py"],
    "": ["main.py", "requirements.txt", "README.md", ".env"]
}

# Placeholder contents for each file (optional)
file_templates = {
    "config.py": "# Bot token, Google Sheets API credentials, admin IDs\n",
    "start.py": "# Handles /start command and welcome message\n",
    "registration.py": "# Manages registration flow\n",
    "payment.py": "# Handles payment uploads and approvals\n",
    "admin.py": "# Admin commands (view, approve, etc.)\n",
    "error.py": "# Error handling and logging\n",
    "sheets.py": "# Google Sheets integration\n",
    "validators.py": "# Input validation (phone, etc.)\n",
    "batch.py": "# Batch number generation\n",
    "main.py": "# Main bot entry point\n",
    "requirements.txt": "# Dependencies\naiogram\npython-dotenv\n",
    "README.md": "# Project documentation\n",
    ".env": "# Environment variables (bot token, etc.)\nBOT_TOKEN=\n"
}

# Create folders and files
for folder, files in project_structure.items():
    if folder:
        os.makedirs(folder, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder, file)
        with open(file_path, "w") as f:
            f.write(file_templates.get(file, ""))

print("✅ Project structure created successfully.")

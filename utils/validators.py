import re

def validate_phone(phone):
    """Validate Ethiopian phone number."""
    pattern = r"^\+251[79]\d{8}$|^0[79]\d{8}$"
    return bool(re.match(pattern, phone))

def validate_name(name):
    """Ensure name is non-empty and contains only letters and spaces."""
    return bool(name and re.match(r"^[a-zA-Zሀ-ፐ\s]+$", name))
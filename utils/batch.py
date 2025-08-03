import random
import string

def generate_batch_number():
    """Generate a unique batch number."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
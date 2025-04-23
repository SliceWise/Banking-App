"""
Utility module for the Banking Application
Contains helper functions used across the application
"""
import os
import sys
import time
import re
import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pause execution until user presses Enter"""
    input("\nPress Enter to continue...")

def get_amount(prompt):
    """Get a valid money amount from user input"""
    while True:
        try:
            amount_str = input(prompt)
            # Replace any commas and ensure proper decimal format
            amount_str = amount_str.replace(',', '')
            
            # Check if the input is in proper money format
            if not re.match(r'^\$?\d+(\.\d{0,2})?$', amount_str):
                print("Please enter a valid amount (e.g., 100 or 100.50)")
                continue
            
            # Remove dollar sign if present
            amount_str = amount_str.replace('$', '')
            
            # Convert to float
            amount = float(amount_str)
            return amount
            
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")

def format_currency(amount):
    """Format a number as currency"""
    return f"${amount:.2f}"

def format_date(date_str):
    """Format an ISO date string to a more readable format"""
    try:
        date_obj = datetime.datetime.fromisoformat(date_str)
        return date_obj.strftime("%B %d, %Y %I:%M %p")
    except ValueError:
        return date_str

def is_valid_email(email):
    """Check if an email address is valid"""
    # Simple email validation regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def generate_random_password(length=12):
    """Generate a random secure password"""
    import random
    import string
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = '!@#$%^&*()-_=+[]{}|;:,.<>?'
    
    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest with random characters from all sets
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    # Shuffle the characters
    random.shuffle(password)
    
    return ''.join(password)

def loading_animation(duration=1, text="Loading"):
    """Display a simple loading animation"""
    animation = "|/-\\"
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        sys.stdout.write(f"\r{text} {animation[i % len(animation)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write(f"\r{text} Complete!")
    sys.stdout.flush()
    print()

def truncate_string(s, max_length=30):
    """Truncate a string to max_length and add ellipsis if needed"""
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."

def confirm_action(prompt="Are you sure you want to proceed? (y/n): "):
    """Get confirmation from the user"""
    response = input(prompt).lower()
    return response in ['y', 'yes']

def validate_account_number(account_number):
    """Validate the format of an account number"""
    # Assuming account numbers are 10-digit numeric strings
    return bool(re.match(r'^\d{10}$', account_number))

def log_error(message):
    """Log an error message to a file"""
    error_dir = "data/logs"
    os.makedirs(error_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().isoformat()
    with open(f"{error_dir}/error_log.txt", "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")

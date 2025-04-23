"""
Storage module for the Banking Application
Handles data persistence for users, accounts, and transactions
"""
import os
import json
import csv
import datetime

# File paths
USERS_FILE = 'data/users.json'
ACCOUNTS_FILE = 'data/accounts.json'
TRANSACTIONS_FILE = 'data/transactions.csv'

def initialize_data_files():
    """Initialize data files if they don't exist"""
    # Create directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Initialize users.json
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize accounts.json
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize transactions.csv with headers
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'transaction_id', 'account_number', 'type', 
                'amount', 'balance', 'date', 'description'
            ])

def load_users():
    """Load users from the JSON file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle missing or corrupted file
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
        return []

def save_users(users):
    """Save users to the JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def load_accounts():
    """Load accounts from the JSON file"""
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle missing or corrupted file
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump([], f)
        return []

def save_accounts(accounts):
    """Save accounts to the JSON file"""
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving accounts: {e}")
        return False

def save_transaction(transaction):
    """Save a transaction to the CSV file"""
    try:
        with open(TRANSACTIONS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                transaction['transaction_id'],
                transaction['account_number'],
                transaction['type'],
                transaction['amount'],
                transaction['balance'],
                transaction['date'],
                transaction['description']
            ])
        return True
    except Exception as e:
        print(f"Error saving transaction: {e}")
        return False

def load_transactions():
    """Load all transactions from the CSV file"""
    transactions = []
    
    try:
        with open(TRANSACTIONS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert amount and balance to float
                row['amount'] = float(row['amount'])
                row['balance'] = float(row['balance'])
                transactions.append(row)
    except FileNotFoundError:
        # Create the file if it doesn't exist
        initialize_data_files()
    
    return transactions

def backup_data():
    """Create a backup of all data files"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"data/backup_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup users.json
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as src, open(f"{backup_dir}/users.json", 'w') as dst:
                dst.write(src.read())
        
        # Backup accounts.json
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as src, open(f"{backup_dir}/accounts.json", 'w') as dst:
                dst.write(src.read())
        
        # Backup transactions.csv
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, 'r') as src, open(f"{backup_dir}/transactions.csv", 'w') as dst:
                dst.write(src.read())
        
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def restore_backup(backup_folder):
    """Restore data from a backup"""
    if not os.path.exists(backup_folder):
        print(f"Backup folder {backup_folder} does not exist.")
        return False
    
    try:
        # Restore users.json
        if os.path.exists(f"{backup_folder}/users.json"):
            with open(f"{backup_folder}/users.json", 'r') as src, open(USERS_FILE, 'w') as dst:
                dst.write(src.read())
        
        # Restore accounts.json
        if os.path.exists(f"{backup_folder}/accounts.json"):
            with open(f"{backup_folder}/accounts.json", 'r') as src, open(ACCOUNTS_FILE, 'w') as dst:
                dst.write(src.read())
        
        # Restore transactions.csv
        if os.path.exists(f"{backup_folder}/transactions.csv"):
            with open(f"{backup_folder}/transactions.csv", 'r') as src, open(TRANSACTIONS_FILE, 'w') as dst:
                dst.write(src.read())
        
        return True
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

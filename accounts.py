"""
Account management module for the Banking Application
Handles creation and management of checking and savings accounts
"""
import uuid
import datetime
import storage
import transactions

def generate_account_number():
    """Generate a unique account number"""
    return str(uuid.uuid4().int)[:10]

def create_account(username, account_type, initial_deposit=0):
    """Create a new account for a user"""
    if account_type not in ['checking', 'savings']:
        return None
    
    account_number = generate_account_number()
    
    # Create the account
    new_account = {
        'account_number': account_number,
        'username': username,
        'account_type': account_type,
        'balance': initial_deposit,
        'created_at': datetime.datetime.now().isoformat(),
        'interest_rate': 0.02 if account_type == 'savings' else 0.001
    }
    
    accounts = storage.load_accounts()
    accounts.append(new_account)
    
    if storage.save_accounts(accounts):
        # Create an initial deposit transaction if there's an initial amount
        if initial_deposit > 0:
            transactions.deposit(account_number, initial_deposit, "Initial deposit")
        return new_account
    return None

def get_account(account_number):
    """Get an account by account number"""
    accounts = storage.load_accounts()
    for account in accounts:
        if account['account_number'] == account_number:
            return account
    return None

def get_accounts_by_user(username):
    """Get all accounts for a specific user"""
    accounts = storage.load_accounts()
    return [account for account in accounts if account['username'] == username]

def update_balance(account_number, amount):
    """Update the balance of an account"""
    accounts = storage.load_accounts()
    
    for i, account in enumerate(accounts):
        if account['account_number'] == account_number:
            new_balance = account['balance'] + amount
            if new_balance < 0:  # Prevent negative balance
                return False
            
            accounts[i]['balance'] = new_balance
            if storage.save_accounts(accounts):
                return True
            return False
    
    return False

def add_interest():
    """Add monthly interest to all savings accounts"""
    accounts = storage.load_accounts()
    updated = False
    
    for i, account in enumerate(accounts):
        if account['account_type'] == 'savings':
            interest_amount = account['balance'] * account['interest_rate'] / 12  # Monthly interest
            accounts[i]['balance'] += interest_amount
            
            # Record interest transaction
            transactions.create_transaction(
                account['account_number'],
                'interest',
                interest_amount,
                accounts[i]['balance'],
                "Monthly interest"
            )
            updated = True
    
    if updated:
        storage.save_accounts(accounts)
        return True
    return False

def close_account(account_number):
    """Close an account (remove it from the system)"""
    accounts = storage.load_accounts()
    
    for i, account in enumerate(accounts):
        if account['account_number'] == account_number:
            if account['balance'] != 0:
                return False  # Can't close account with remaining balance
            
            del accounts[i]
            if storage.save_accounts(accounts):
                return True
            return False
    
    return False

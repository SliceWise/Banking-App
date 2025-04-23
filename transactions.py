"""
Transaction module for the Banking Application
Handles deposits, withdrawals, transfers, and transaction history
"""
import datetime
import uuid
import storage
import accounts

def create_transaction(account_number, transaction_type, amount, balance, description=None):
    """Create and store a new transaction"""
    transaction = {
        'transaction_id': str(uuid.uuid4()),
        'account_number': account_number,
        'type': transaction_type,
        'amount': amount,
        'balance': balance,
        'date': datetime.datetime.now().isoformat(),
        'description': description or ''
    }
    
    storage.save_transaction(transaction)
    return transaction

def deposit(account_number, amount, description=None):
    """Make a deposit to an account"""
    if amount <= 0:
        return None
    
    account = accounts.get_account(account_number)
    if not account:
        return None
    
    # Update account balance
    if accounts.update_balance(account_number, amount):
        # Get updated account
        updated_account = accounts.get_account(account_number)
        
        # Create transaction record
        transaction = create_transaction(
            account_number,
            'deposit',
            amount,
            updated_account['balance'],
            description
        )
        
        return transaction
    
    return None

def withdraw(account_number, amount, description=None):
    """Make a withdrawal from an account"""
    if amount <= 0:
        return None
    
    account = accounts.get_account(account_number)
    if not account or account['balance'] < amount:
        return None
    
    # Update account balance (negative amount for withdrawal)
    if accounts.update_balance(account_number, -amount):
        # Get updated account
        updated_account = accounts.get_account(account_number)
        
        # Create transaction record
        transaction = create_transaction(
            account_number,
            'withdrawal',
            amount,  # Store as positive amount
            updated_account['balance'],
            description
        )
        
        return transaction
    
    return None

def transfer(from_account, to_account, amount, description=None):
    """Transfer money between accounts"""
    if amount <= 0:
        return None
    
    # First withdraw from source account
    withdrawal = withdraw(from_account, amount, f"Transfer to {to_account}")
    if not withdrawal:
        return None
    
    # Then deposit to destination account
    deposit_desc = f"Transfer from {from_account}"
    deposit_result = deposit(to_account, amount, deposit_desc)
    
    if deposit_result:
        return {
            'withdrawal': withdrawal,
            'deposit': deposit_result,
            'amount': amount,
            'date': datetime.datetime.now().isoformat()
        }
    
    # If deposit fails, we need to rollback the withdrawal
    deposit(from_account, amount, "Failed transfer rollback")
    return None

def get_account_transactions(account_number):
    """Get all transactions for a specific account"""
    all_transactions = storage.load_transactions()
    account_transactions = [tx for tx in all_transactions if tx['account_number'] == account_number]
    
    # Sort by date (newest first)
    account_transactions.sort(key=lambda x: x['date'], reverse=True)
    return account_transactions

def get_transactions_by_date_range(account_number, start_date, end_date):
    """Get transactions within a specific date range"""
    all_transactions = get_account_transactions(account_number)
    
    # Convert string dates to datetime objects for comparison
    start = datetime.datetime.fromisoformat(start_date)
    end = datetime.datetime.fromisoformat(end_date)
    
    filtered_transactions = []
    for tx in all_transactions:
        tx_date = datetime.datetime.fromisoformat(tx['date'])
        if start <= tx_date <= end:
            filtered_transactions.append(tx)
    
    return filtered_transactions

def get_transactions_by_type(account_number, transaction_type):
    """Get transactions of a specific type"""
    all_transactions = get_account_transactions(account_number)
    return [tx for tx in all_transactions if tx['type'] == transaction_type]

#!/usr/bin/env python3
"""
Banking Application CLI - Main Entry Point
"""
import os
import sys
import argparse
from getpass import getpass
import auth
import accounts
import transactions
import reports
import storage
import utils

def setup():
    """Initialize application data directories and files"""
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Initialize data files if they don't exist
    storage.initialize_data_files()
    print("Banking application initialized successfully.")

def login_menu():
    """Display login menu and handle authentication"""
    while True:
        utils.clear_screen()
        print("===== BANKING APPLICATION =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            username = input("Username: ")
            password = getpass("Password: ")
            user = auth.login(username, password)
            if user:
                print(f"Welcome back, {user['name']}!")
                utils.pause()
                main_menu(user)
            else:
                print("Invalid username or password.")
                utils.pause()
        
        elif choice == '2':
            username = input("Choose a username: ")
            if auth.user_exists(username):
                print("Username already exists. Please choose another.")
                utils.pause()
                continue
                
            password = getpass("Choose a password: ")
            confirm_password = getpass("Confirm password: ")
            
            if password != confirm_password:
                print("Passwords do not match.")
                utils.pause()
                continue
                
            name = input("Enter your full name: ")
            email = input("Enter your email: ")
            
            user = auth.register(username, password, name, email)
            if user:
                print(f"Welcome, {user['name']}! Account created successfully.")
                utils.pause()
                main_menu(user)
            else:
                print("Registration failed. Please try again.")
                utils.pause()
        
        elif choice == '3':
            print("Thank you for using the Banking Application.")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")
            utils.pause()

def main_menu(user):
    """Display main application menu"""
    while True:
        utils.clear_screen()
        print(f"===== MAIN MENU | Welcome, {user['name']} =====")
        print("1. View Accounts")
        print("2. Create New Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Transaction History")
        print("7. Reports")
        print("8. Logout")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            view_accounts(user)
        elif choice == '2':
            create_account(user)
        elif choice == '3':
            make_deposit(user)
        elif choice == '4':
            make_withdrawal(user)
        elif choice == '5':
            make_transfer(user)
        elif choice == '6':
            view_transaction_history(user)
        elif choice == '7':
            reports_menu(user)
        elif choice == '8':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")
            utils.pause()

def view_accounts(user):
    """View all accounts for the user"""
    utils.clear_screen()
    print("===== YOUR ACCOUNTS =====")
    user_accounts = accounts.get_accounts_by_user(user['username'])
    
    if not user_accounts:
        print("You don't have any accounts yet.")
    else:
        for idx, account in enumerate(user_accounts, 1):
            print(f"{idx}. {account['account_number']} ({account['account_type'].capitalize()}) - ${account['balance']:.2f}")
    
    utils.pause()

def create_account(user):
    """Create a new account for the user"""
    utils.clear_screen()
    print("===== CREATE NEW ACCOUNT =====")
    print("Account Types:")
    print("1. Checking")
    print("2. Savings")
    
    choice = input("Select account type (1-2): ")
    
    if choice == '1':
        account_type = 'checking'
    elif choice == '2':
        account_type = 'savings'
    else:
        print("Invalid choice.")
        utils.pause()
        return
    
    initial_deposit = utils.get_amount("Initial deposit amount: $")
    if initial_deposit < 0:
        print("Initial deposit cannot be negative.")
        utils.pause()
        return
    
    account = accounts.create_account(user['username'], account_type, initial_deposit)
    if account:
        print(f"Account created successfully! Account number: {account['account_number']}")
    else:
        print("Failed to create account. Please try again.")
    
    utils.pause()

def make_deposit(user):
    """Make a deposit to an account"""
    utils.clear_screen()
    print("===== DEPOSIT =====")
    user_accounts = accounts.get_accounts_by_user(user['username'])
    
    if not user_accounts:
        print("You don't have any accounts yet.")
        utils.pause()
        return
    
    account = select_account(user_accounts)
    if not account:
        return
    
    amount = utils.get_amount("Enter deposit amount: $")
    if amount <= 0:
        print("Deposit amount must be positive.")
        utils.pause()
        return
    
    transaction = transactions.deposit(account['account_number'], amount)
    if transaction:
        print(f"Deposit successful. New balance: ${accounts.get_account(account['account_number'])['balance']:.2f}")
    else:
        print("Deposit failed. Please try again.")
    
    utils.pause()

def make_withdrawal(user):
    """Make a withdrawal from an account"""
    utils.clear_screen()
    print("===== WITHDRAWAL =====")
    user_accounts = accounts.get_accounts_by_user(user['username'])
    
    if not user_accounts:
        print("You don't have any accounts yet.")
        utils.pause()
        return
    
    account = select_account(user_accounts)
    if not account:
        return
    
    amount = utils.get_amount("Enter withdrawal amount: $")
    if amount <= 0:
        print("Withdrawal amount must be positive.")
        utils.pause()
        return
    
    transaction = transactions.withdraw(account['account_number'], amount)
    if transaction:
        print(f"Withdrawal successful. New balance: ${accounts.get_account(account['account_number'])['balance']:.2f}")
    else:
        print("Withdrawal failed. Insufficient funds or invalid amount.")
    
    utils.pause()

def make_transfer(user):
    """Transfer money between accounts"""
    utils.clear_screen()
    print("===== TRANSFER =====")
    user_accounts = accounts.get_accounts_by_user(user['username'])
    
    if not user_accounts or len(user_accounts) < 2:
        print("You need at least two accounts to make a transfer.")
        utils.pause()
        return
    
    print("Select source account:")
    from_account = select_account(user_accounts)
    if not from_account:
        return
    
    # Filter out the source account from the list
    remaining_accounts = [acc for acc in user_accounts if acc['account_number'] != from_account['account_number']]
    
    print("Select destination account:")
    to_account = select_account(remaining_accounts)
    if not to_account:
        return
    
    amount = utils.get_amount("Enter transfer amount: $")
    if amount <= 0:
        print("Transfer amount must be positive.")
        utils.pause()
        return
    
    transaction = transactions.transfer(from_account['account_number'], to_account['account_number'], amount)
    if transaction:
        from_acc = accounts.get_account(from_account['account_number'])
        to_acc = accounts.get_account(to_account['account_number'])
        print(f"Transfer successful.")
        print(f"Source account balance: ${from_acc['balance']:.2f}")
        print(f"Destination account balance: ${to_acc['balance']:.2f}")
    else:
        print("Transfer failed. Insufficient funds or invalid amount.")
    
    utils.pause()

def view_transaction_history(user):
    """View transaction history for an account"""
    utils.clear_screen()
    print("===== TRANSACTION HISTORY =====")
    user_accounts = accounts.get_accounts_by_user(user['username'])
    
    if not user_accounts:
        print("You don't have any accounts yet.")
        utils.pause()
        return
    
    account = select_account(user_accounts)
    if not account:
        return
    
    print(f"Transactions for account {account['account_number']}:")
    transaction_list = transactions.get_account_transactions(account['account_number'])
    
    if not transaction_list:
        print("No transactions found for this account.")
    else:
        for idx, tx in enumerate(transaction_list, 1):
            print(f"{idx}. {tx['date']} - {tx['type'].capitalize()}: ${tx['amount']:.2f} - Balance: ${tx['balance']:.2f}")
            if tx['description']:
                print(f"   Description: {tx['description']}")
    
    utils.pause()

def reports_menu(user):
    """Display reports menu"""
    while True:
        utils.clear_screen()
        print("===== REPORTS =====")
        print("1. Account Summary")
        print("2. Monthly Spending")
        print("3. Spending by Category")
        print("4. Income vs. Expenses")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            reports.account_summary(user['username'])
        elif choice == '2':
            reports.monthly_spending(user['username'])
        elif choice == '3':
            reports.spending_by_category(user['username'])
        elif choice == '4':
            reports.income_vs_expenses(user['username'])
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
        
        utils.pause()

def select_account(user_accounts):
    """Helper function to select an account from a list"""
    for idx, account in enumerate(user_accounts, 1):
        print(f"{idx}. {account['account_number']} ({account['account_type'].capitalize()}) - ${account['balance']:.2f}")
    
    try:
        choice = int(input(f"Select account (1-{len(user_accounts)}): "))
        if 1 <= choice <= len(user_accounts):
            return user_accounts[choice - 1]
        else:
            print("Invalid choice.")
            utils.pause()
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        utils.pause()
        return None

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Banking Application CLI')
    parser.add_argument('--setup', action='store_true', help='Initialize application data')
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if args.setup:
        setup()
        return
    
    storage.initialize_data_files()  # Ensure files exist
    login_menu()

if __name__ == "__main__":
    main()

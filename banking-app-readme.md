# Banking Application CLI

A command-line interface banking application that allows users to manage accounts, perform transactions, and generate financial reports.

## Overview

This Banking Application is a feature-rich command-line application that simulates basic banking operations. It provides functionalities for account management, transactions, and financial reporting with data visualization capabilities.

## Features

- **User Authentication**
  - User registration and login system
  - Secure password hashing

- **Account Management**
  - Create checking and savings accounts
  - View account details and balances
  - Close accounts

- **Transaction Processing**
  - Deposits and withdrawals
  - Fund transfers between accounts
  - Transaction history viewing

- **Financial Reports**
  - Account summary
  - Monthly spending analysis
  - Spending by category (with automatic categorization)
  - Income vs expenses comparison

- **Data Visualization**
  - Pie charts for balance distribution and spending categories
  - Bar charts for monthly comparisons
  - Line charts for income vs expenses over time

- **Data Storage and Security**
  - Persistent data storage using JSON and CSV files
  - Backup and restore functionality

## Installation

### Prerequisites

- Python 3.6 or higher
- Matplotlib (for data visualization)

### Setup

1. Clone the repository or download the source code

2. Install required dependencies:
```bash
pip install matplotlib
```

3. Initialize the application:
```bash
python main.py --setup
```

## Usage

### Starting the Application

```bash
python main.py
```

### User Registration

1. Select "Register" from the login menu
2. Enter username, password, full name, and email
3. Follow the prompts to create your first account

### Account Operations

- **Create Account**: Create checking or savings accounts with optional initial deposits
- **View Accounts**: See all your accounts with their current balances
- **Deposit**: Add funds to your account
- **Withdraw**: Remove funds from your account
- **Transfer**: Move funds between your accounts
- **Transaction History**: View a chronological list of all account transactions

### Financial Reports

- **Account Summary**: Overview of all accounts with balances and recent transactions
- **Monthly Spending**: Compare current month's spending with previous month
- **Spending by Category**: Automatic categorization of expenses with visual breakdown
- **Income vs Expenses**: Track income and expenses over the last 6 months

## Data Structure

The application stores data in the following files:

- `data/users.json`: User information and credentials
- `data/accounts.json`: Account details and balances
- `data/transactions.csv`: Transaction records
- `data/plots/`: Generated charts and visualizations
- `data/logs/`: Error logs (if any)

## Modules

- **main.py**: Main entry point and menu system
- **auth.py**: User authentication and registration
- **accounts.py**: Account creation and management
- **transactions.py**: Transaction processing
- **reports.py**: Financial report generation
- **plotting.py**: Data visualization utilities
- **storage.py**: Data persistence and file operations
- **utils.py**: Helper functions and utilities

## Security Features

- Passwords are securely hashed with salt
- Prevention of negative balances
- Data validation for monetary inputs
- Error logging

## Backup and Restore

The application includes functionality to create backups of all data files, which can be restored if needed. This feature is implemented in the `storage.py` module.

## Extension and Customization

The modular design of the application makes it easy to extend with additional features:

- Add new account types
- Implement additional reports
- Create custom visualization options
- Add new transaction categories

## Troubleshooting

If you encounter any issues:

1. Check that all required dependencies are installed
2. Ensure the application was properly initialized with `--setup`
3. Verify that the `data` directory and its contents have proper permissions
4. Consult the error logs in `data/logs/error_log.txt`

## License

This project is available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- This application uses Matplotlib for data visualization
- UUID library for generating unique identifiers
- CSV and JSON modules for data persistence

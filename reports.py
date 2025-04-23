"""
Reports module for the Banking Application
Generates financial reports and visualizations
"""
import datetime
import calendar
from collections import defaultdict
import plotting
import storage
import accounts
import transactions
import utils

def account_summary(username):
    """Generate an account summary report for a user"""
    user_accounts = accounts.get_accounts_by_user(username)
    
    if not user_accounts:
        print("No accounts found for this user.")
        return
    
    utils.clear_screen()
    print("===== ACCOUNT SUMMARY REPORT =====")
    
    total_balance = 0
    for account in user_accounts:
        print(f"\nAccount: {account['account_number']} ({account['account_type'].capitalize()})")
        print(f"Balance: ${account['balance']:.2f}")
        
        if account['account_type'] == 'savings':
            print(f"Interest Rate: {account['interest_rate'] * 100:.2f}%")
            monthly_interest = account['balance'] * account['interest_rate'] / 12
            print(f"Est. Monthly Interest: ${monthly_interest:.2f}")
        
        # Get recent transactions
        recent_txs = transactions.get_account_transactions(account['account_number'])[:5]
        
        if recent_txs:
            print("\nRecent Transactions:")
            for tx in recent_txs:
                print(f"  {tx['date'][:10]} - {tx['type'].capitalize()}: ${tx['amount']:.2f}")
        
        total_balance += account['balance']
    
    print(f"\nTotal Balance Across All Accounts: ${total_balance:.2f}")
    
    # Generate a balance pie chart
    if len(user_accounts) > 1:
        labels = [f"{acc['account_type'].capitalize()} ({acc['account_number'][-4:]})" for acc in user_accounts]
        values = [acc['balance'] for acc in user_accounts]
        plotting.pie_chart(labels, values, "Balance Distribution")

def monthly_spending(username):
    """Generate a monthly spending report"""
    utils.clear_screen()
    print("===== MONTHLY SPENDING REPORT =====")
    
    user_accounts = accounts.get_accounts_by_user(username)
    if not user_accounts:
        print("No accounts found for this user.")
        return
    
    # Get current month and year
    now = datetime.datetime.now()
    year, month = now.year, now.month
    
    # Get last month (for comparison)
    if month == 1:
        last_month = 12
        last_year = year - 1
    else:
        last_month = month - 1
        last_year = year
    
    # Create date range strings
    last_month_start = f"{last_year}-{last_month:02d}-01T00:00:00"
    last_month_end = f"{last_year}-{last_month:02d}-{calendar.monthrange(last_year, last_month)[1]:02d}T23:59:59"
    
    this_month_start = f"{year}-{month:02d}-01T00:00:00"
    this_month_end = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}T23:59:59"
    
    # Get spending for each account
    total_this_month = 0
    total_last_month = 0
    
    print(f"\nSpending for {calendar.month_name[month]} {year}:")
    
    for account in user_accounts:
        account_number = account['account_number']
        
        # Get withdrawals for this month
        this_month_txs = transactions.get_transactions_by_date_range(
            account_number, this_month_start, this_month_end)
        this_month_withdrawals = [tx for tx in this_month_txs if tx['type'] == 'withdrawal']
        
        # Get withdrawals for last month
        last_month_txs = transactions.get_transactions_by_date_range(
            account_number, last_month_start, last_month_end)
        last_month_withdrawals = [tx for tx in last_month_txs if tx['type'] == 'withdrawal']
        
        # Calculate totals
        this_month_total = sum(tx['amount'] for tx in this_month_withdrawals)
        last_month_total = sum(tx['amount'] for tx in last_month_withdrawals)
        
        print(f"\nAccount: {account_number} ({account['account_type'].capitalize()})")
        print(f"This Month Spending: ${this_month_total:.2f}")
        print(f"Last Month Spending: ${last_month_total:.2f}")
        
        # Calculate change percentage
        if last_month_total > 0:
            change_pct = ((this_month_total - last_month_total) / last_month_total) * 100
            print(f"Change: {change_pct:+.2f}%")
        
        total_this_month += this_month_total
        total_last_month += last_month_total
    
    print(f"\nTotal Spending Across All Accounts:")
    print(f"This Month: ${total_this_month:.2f}")
    print(f"Last Month: ${total_last_month:.2f}")
    
    if total_last_month > 0:
        total_change_pct = ((total_this_month - total_last_month) / total_last_month) * 100
        print(f"Overall Change: {total_change_pct:+.2f}%")
    
    # Generate bar chart comparing this month to last month
    if total_this_month > 0 or total_last_month > 0:
        labels = [f"Last Month ({calendar.month_name[last_month]})", 
                 f"This Month ({calendar.month_name[month]})"]
        values = [total_last_month, total_this_month]
        plotting.bar_chart(labels, values, "Monthly Spending Comparison")

def spending_by_category(username):
    """Generate a spending by category report based on transaction descriptions"""
    utils.clear_screen()
    print("===== SPENDING BY CATEGORY REPORT =====")
    
    user_accounts = accounts.get_accounts_by_user(username)
    if not user_accounts:
        print("No accounts found for this user.")
        return
    
    # Define categories and their keywords
    categories = {
        'Food': ['restaurant', 'grocery', 'food', 'cafe', 'coffee'],
        'Transport': ['gas', 'uber', 'lyft', 'taxi', 'transit', 'fuel', 'parking'],
        'Shopping': ['amazon', 'walmart', 'target', 'purchase', 'buy', 'store'],
        'Bills': ['bill', 'utility', 'electric', 'water', 'rent', 'insurance'],
        'Entertainment': ['movie', 'game', 'netflix', 'spotify', 'theater', 'concert'],
        'Other': []  # Catch-all category
    }
    
    # Get current month
    now = datetime.datetime.now()
    year, month = now.year, now.month
    
    month_start = f"{year}-{month:02d}-01T00:00:00"
    month_end = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}T23:59:59"
    
    # Initialize spending by category
    category_spending = defaultdict(float)
    
    # Process all withdrawals for all accounts
    for account in user_accounts:
        account_number = account['account_number']
        
        # Get withdrawals for this month
        month_txs = transactions.get_transactions_by_date_range(
            account_number, month_start, month_end)
        withdrawals = [tx for tx in month_txs if tx['type'] == 'withdrawal']
        
        # Categorize each withdrawal
        for tx in withdrawals:
            categorized = False
            description = tx['description'].lower() if tx['description'] else ''
            
            for category, keywords in categories.items():
                if any(keyword in description for keyword in keywords):
                    category_spending[category] += tx['amount']
                    categorized = True
                    break
            
            if not categorized:
                category_spending['Other'] += tx['amount']
    
    # Print the report
    print(f"\nSpending by Category for {calendar.month_name[month]} {year}:")
    
    total_spending = sum(category_spending.values())
    
    if total_spending == 0:
        print("No spending data found for this month.")
        return
    
    for category, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
        if amount > 0:
            percentage = (amount / total_spending) * 100
            print(f"{category}: ${amount:.2f} ({percentage:.1f}%)")
    
    print(f"\nTotal: ${total_spending:.2f}")
    
    # Generate pie chart
    if category_spending:
        # Remove categories with 0 spending
        filtered_categories = {k: v for k, v in category_spending.items() if v > 0}
        plotting.pie_chart(
            list(filtered_categories.keys()),
            list(filtered_categories.values()),
            "Spending by Category"
        )

def income_vs_expenses(username):
    """Generate an income vs expenses report"""
    utils.clear_screen()
    print("===== INCOME VS EXPENSES REPORT =====")
    
    user_accounts = accounts.get_accounts_by_user(username)
    if not user_accounts:
        print("No accounts found for this user.")
        return
    
    # Get data for the last 6 months
    now = datetime.datetime.now()
    
    # Calculate months to analyze
    months_data = []
    for i in range(5, -1, -1):  # Last 6 months
        year = now.year
        month = now.month - i
        
        if month <= 0:
            month += 12
            year -= 1
        
        months_data.append((year, month))
    
    # Initialize data structures
    monthly_income = []
    monthly_expenses = []
    month_labels = []
    
    print("\nIncome vs Expenses Over Last 6 Months:")
    
    # Process each month
    for year, month in months_data:
        month_start = f"{year}-{month:02d}-01T00:00:00"
        month_end = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}T23:59:59"
        
        month_income = 0
        month_expenses = 0
        
        for account in user_accounts:
            account_number = account['account_number']
            
            # Get transactions for this month
            month_txs = transactions.get_transactions_by_date_range(
                account_number, month_start, month_end)
            
            # Separate deposits and withdrawals
            deposits = [tx for tx in month_txs if tx['type'] == 'deposit']
            withdrawals = [tx for tx in month_txs if tx['type'] == 'withdrawal']
            
            # Calculate totals
            month_income += sum(tx['amount'] for tx in deposits)
            month_expenses += sum(tx['amount'] for tx in withdrawals)
        
        # Add to monthly data
        monthly_income.append(month_income)
        monthly_expenses.append(month_expenses)
        month_labels.append(f"{calendar.month_name[month][:3]} {year}")
        
        print(f"\n{calendar.month_name[month]} {year}:")
        print(f"  Income: ${month_income:.2f}")
        print(f"  Expenses: ${month_expenses:.2f}")
        net = month_income - month_expenses
        print(f"  Net: ${net:.2f} ({'Profit' if net >= 0 else 'Loss'})")
    
    # Generate line chart
    plotting.line_chart(month_labels, [monthly_income, monthly_expenses], 
                        ["Income", "Expenses"], "Income vs Expenses")
    
    # Calculate totals
    total_income = sum(monthly_income)
    total_expenses = sum(monthly_expenses)
    net_total = total_income - total_expenses
    
    print(f"\nSummary for Last 6 Months:")
    print(f"  Total Income: ${total_income:.2f}")
    print(f"  Total Expenses: ${total_expenses:.2f}")
    print(f"  Net: ${net_total:.2f} ({'Profit' if net_total >= 0 else 'Loss'})")
    
    # Calculate averages
    avg_income = total_income / 6
    avg_expenses = total_expenses / 6
    print(f"  Average Monthly Income: ${avg_income:.2f}")
    print(f"  Average Monthly Expenses: ${avg_expenses:.2f}")
    
    # Savings rate
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
        print(f"  Savings Rate: {savings_rate:.2f}%")

"""
Stock Portfolio Tracker

A modular Python script to track stock investments, validate user input, 
calculate portfolio values, display styled console output, and save reports.
"""

from datetime import datetime
import os


# ==========================================
# BACKEND LOGIC (Data & Business Logic)
# ==========================================

def get_stock_prices():
    """
    Returns a dictionary of hardcoded stock prices.
    
    Returns:
        dict: Mapping of stock symbol (str) to price per share (float).
    """
    return {
        "AAPL": 180.00,
        "TSLA": 250.00,
        "GOOGL": 140.00,
        "AMZN": 145.00,
        "MSFT": 330.00,
        "NVDA": 480.00,
        "NFLX": 440.00
    }


def validate_stock(symbol, stock_prices):
    """
    Validates whether an entered stock symbol exists in the stock price dictionary.
    
    Args:
        symbol (str): The stock ticker symbol entered by the user.
        stock_prices (dict): Available stock prices.
        
    Returns:
        bool: True if symbol exists (case-insensitive check), False otherwise.
    """
    if not symbol:
        return False
    return symbol.strip().upper() in stock_prices


def calculate_investment(portfolio, stock_prices):
    """
    Calculates subtotal per stock and grand total investment value.
    
    Args:
        portfolio (dict): Mapping of stock symbol (uppercase str) to quantity (int).
        stock_prices (dict): Mapping of stock symbol to price (float).
        
    Returns:
        tuple: (portfolio_details, grand_total)
            - portfolio_details (list of dicts): Breakdown per stock including symbol, quantity, price, and subtotal.
            - grand_total (float): Sum of all stock subtotals.
    """
    portfolio_details = []
    grand_total = 0.0

    for symbol, quantity in portfolio.items():
        price = stock_prices.get(symbol, 0.0)
        subtotal = price * quantity
        grand_total += subtotal
        
        portfolio_details.append({
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        })

    return portfolio_details, grand_total


def save_results(portfolio_details, grand_total, filename=None, file_format="txt"):
    """
    Saves portfolio summary to a .txt or .csv file with a timestamp.
    
    Args:
        portfolio_details (list): List of stock breakdown dictionaries.
        grand_total (float): Total investment value.
        filename (str, optional): Custom filename. Defaults to portfolio_summary.txt or .csv.
        file_format (str): 'txt' or 'csv'.
        
    Returns:
        str: Absolute path of the saved file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_format = file_format.lower().strip()

    if not filename:
        filename = f"portfolio_summary.{file_format}"

    filepath = os.path.abspath(filename)

    if file_format == "csv":
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write(f"# Portfolio Summary Generated on {timestamp}\n")
            f.write("Stock Symbol,Quantity,Price ($),Subtotal ($)\n")
            for item in portfolio_details:
                f.write(f"{item['symbol']},{item['quantity']},{item['price']:.2f},{item['subtotal']:.2f}\n")
            f.write(f"GRAND TOTAL,,,{grand_total:.2f}\n")
    else:  # TXT default
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"           STOCK PORTFOLIO SUMMARY REPORT\n")
            f.write(f"           Generated: {timestamp}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"{'Stock':<10} {'Quantity':<10} {'Price ($)':<12} {'Subtotal ($)':<15}\n")
            f.write("-" * 60 + "\n")
            for item in portfolio_details:
                f.write(f"{item['symbol']:<10} {item['quantity']:<10} ${item['price']:<11.2f} ${item['subtotal']:<14.2f}\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'GRAND TOTAL':<33} ${grand_total:,.2f}\n")
            f.write("=" * 60 + "\n")

    return filepath


# ==========================================
# FRONTEND LOGIC (Console Interface & View)
# ==========================================

def display_welcome():
    """Prints a styled welcome message."""
    print("=" * 60)
    print("        WELCOME TO THE PYTHON STOCK PORTFOLIO TRACKER")
    print("=" * 60)
    print("Track your stock investments effortlessly!\n")


def display_stock_list(stock_prices):
    """
    Displays available stocks and their prices in a formatted table.
    
    Args:
        stock_prices (dict): Hardcoded stock dictionary.
    """
    print("Available Stocks for Tracking:")
    print("-" * 35)
    print(f"{'Ticker Symbol':<18} | {'Price ($)':<12}")
    print("-" * 35)
    for symbol, price in stock_prices.items():
        print(f"{symbol:<18} | ${price:>10.2f}")
    print("-" * 35)
    print()


def get_user_portfolio(stock_prices):
    """
    Prompts user to input stock names and quantities in a loop.
    Stops when the user types 'done' or enters an empty value.
    Validates stock names and quantities gracefully.
    
    Args:
        stock_prices (dict): Available stock prices.
        
    Returns:
        dict: Mapping of stock symbol to cumulative quantity.
    """
    portfolio = {}
    print("Instructions:")
    print("  * Enter a stock ticker symbol to add shares to your portfolio.")
    print("  * Type 'done' (or press Enter without input) when finished.\n")

    while True:
        symbol_input = input("Enter Stock Symbol (or 'done' to finish): ").strip()

        # Exit condition: empty string or 'done'
        if not symbol_input or symbol_input.lower() == "done":
            break

        # Validate stock symbol
        if not validate_stock(symbol_input, stock_prices):
            print(f"[!] Error: '{symbol_input}' is not available in our stock dictionary.")
            print(f"    Available symbols: {', '.join(stock_prices.keys())}\n")
            continue

        symbol = symbol_input.upper()

        # Prompt and validate quantity input
        while True:
            quantity_input = input(f"Enter Quantity for {symbol}: ").strip()
            
            if not quantity_input:
                print("[!] Quantity cannot be empty. Please enter a valid number.\n")
                continue
                
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("[!] Error: Quantity must be a positive integer greater than zero.\n")
                    continue
                break
            except ValueError:
                print("[!] Error: Please enter a valid whole integer for quantity.\n")

        # Accumulate quantity if stock was already entered previously
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"[+] Added {quantity} shares of {symbol}. (Total {symbol} shares: {portfolio[symbol]})\n")

    return portfolio


def display_summary(portfolio_details, grand_total):
    """
    Displays a clean summary table in the console.
    
    Args:
        portfolio_details (list): Calculated portfolio list.
        grand_total (float): Sum of all investments.
    """
    print("\n" + "=" * 62)
    print("                 PORTFOLIO INVESTMENT SUMMARY")
    print("=" * 62)

    if not portfolio_details:
        print("No stocks were added to your portfolio.")
        print("=" * 62 + "\n")
        return

    print(f"{'Stock':<10} | {'Quantity':<10} | {'Price ($)':<12} | {'Subtotal ($)':<16}")
    print("-" * 62)
    
    for item in portfolio_details:
        print(f"{item['symbol']:<10} | {item['quantity']:<10} | ${item['price']:<11.2f} | ${item['subtotal']:<15.2f}")
        
    print("-" * 62)
    print(f"{'GRAND TOTAL INVESTMENT VALUE:':<37} ${grand_total:,.2f}")
    print("=" * 62 + "\n")


def prompt_save_option(portfolio_details, grand_total):
    """
    Prompts user whether to save the summary report to a file (.txt or .csv).
    
    Args:
        portfolio_details (list): Portfolio items list.
        grand_total (float): Grand total value.
    """
    if not portfolio_details:
        return

    save_choice = input("Would you like to save this summary report to a file? (y/n): ").strip().lower()
    if save_choice in ["y", "yes"]:
        print("\nChoose file format:")
        print("1. Text File (.txt)")
        print("2. CSV File (.csv)")
        fmt_choice = input("Enter choice (1 or 2, default 1): ").strip()
        
        file_format = "csv" if fmt_choice == "2" else "txt"
        saved_path = save_results(portfolio_details, grand_total, file_format=file_format)
        print(f"\n[+] Portfolio summary successfully saved to:\n    {saved_path}\n")


# ==========================================
# MAIN ENTRY POINT
# ==========================================

def main():
    """Ties backend and frontend together into an interactive workflow."""
    display_welcome()
    
    # Load backend data
    stock_prices = get_stock_prices()
    
    # Display frontend information
    display_stock_list(stock_prices)
    
    # Get portfolio input from user
    portfolio = get_user_portfolio(stock_prices)
    
    # Calculate backend results
    portfolio_details, grand_total = calculate_investment(portfolio, stock_prices)
    
    # Display summary report
    display_summary(portfolio_details, grand_total)
    
    # Option to save results
    prompt_save_option(portfolio_details, grand_total)
    
    print("Thank you for using Stock Portfolio Tracker!")


if __name__ == "__main__":
    main()
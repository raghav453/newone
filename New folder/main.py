import time
import requests
import yfinance as yf
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

def get_crypto_price(crypto_id):
    """Fetches live crypto price from CoinGecko API."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data[crypto_id]['usd']
    except Exception as e:
        return None

def get_stock_price(ticker):
    """Fetches live stock price using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        # fast_info is usually faster than .info
        return stock.fast_info['last_price']
    except Exception as e:
        return None

def display_dashboard(assets):
    """Prints the formatted dashboard."""
    print("\033c", end="") # Clears terminal
    print(Fore.CYAN + Style.BRIGHT + "="*40)
    print(f"   MARKET WATCH CLI  |  {datetime.now().strftime('%H:%M:%S')}")
    print(Fore.CYAN + "="*40 + "\n")

    print(f"{'ASSET':<15} {'TYPE':<10} {'PRICE (USD)':<15}")
    print("-" * 40)

    for name, details in assets.items():
        price = 0
        if details['type'] == 'Crypto':
            price = get_crypto_price(details['ticker'])
        elif details['type'] == 'Stock':
            price = get_stock_price(details['ticker'])
        
        if price:
            color = Fore.GREEN
            print(f"{color}{name:<15} {details['type']:<10} ${price:,.2f}")
        else:
            print(f"{Fore.RED}{name:<15} {details['type']:<10} ERROR")

    print("\n" + Fore.YELLOW + "Press Ctrl+C to exit...")

def main():
    # CONFIGURATION: Add your favorite assets here
    my_assets = {
        "Bitcoin": {"type": "Crypto", "ticker": "bitcoin"},
        "Ethereum": {"type": "Crypto", "ticker": "ethereum"},
        "Apple":    {"type": "Stock",  "ticker": "AAPL"},
        "Tesla":    {"type": "Stock",  "ticker": "TSLA"},
        "Google":   {"type": "Stock",  "ticker": "GOOGL"},
    }

    try:
        while True:
            display_dashboard(my_assets)
            time.sleep(10) # Updates every 10 seconds
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting Market Watch...")

if __name__ == "__main__":
    main()
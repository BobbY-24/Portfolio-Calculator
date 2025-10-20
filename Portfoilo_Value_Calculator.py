import json
from bs4 import BeautifulSoup
import re
import requests
import csv
import tools
import yfinance as yf
import openpyxl
import sys
from datetime import datetime, timedelta
print(sys.executable)
print(sys.version)



def calculate_total_gain(transactions):
    total_gain = 0
    total_investment = 0
    total_current_value = 0

    print(f"{'Stock':<8}{'Shares':<8}{'Buy Price':<12}{'Now Price':<12}"
          f"{'Investment':<14}{'Current Value':<16}{'Gain ($)':<12}{'Gain (%)'}")
    print("-" * 90)

    for t in transactions:
        stock_code = t["stock_code"]
        shares = t["shares"]
        purchase_date = t["purchase_date"]

        try:
            stock = yf.Ticker(stock_code)

            # handle weekends/holidays by looking at up to 7 days after purchase_date
            start_date = datetime.strptime(purchase_date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=7)

            history = stock.history(start=start_date, end=end_date)
            if history.empty:
                print(f"No data for {stock_code} around {purchase_date}")
                continue

            purchase_price = history['Close'].iloc[0]
            current_price = stock.history(period="1d")['Close'].iloc[0]

            investment = purchase_price * shares
            current_value = current_price * shares
            gain = current_value - investment
            gain_pct = (gain / investment) * 100

            total_investment += investment
            total_current_value += current_value
            total_gain += gain

            print(f"{stock_code:<8}{shares:<8}{purchase_price:<12.2f}{current_price:<12.2f}"
                  f"{investment:<14.2f}{current_value:<16.2f}{gain:<12.2f}{gain_pct:.2f}%")

        except Exception as e:
            print(f"Error retrieving data for {stock_code}: {e}")

    print("-" * 90)
    print(f"{'TOTAL':<28}{total_investment:<14.2f}{total_current_value:<16.2f}"
          f"{total_gain:<12.2f}{(total_gain/total_investment*100):.2f}%")

if __name__ == "__main__":
    # Load portfolio data from JSON file
    with open("portfolio.json", "r") as f:
        transactions = json.load(f)

    calculate_total_gain(transactions)
            

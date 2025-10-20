import json

def create_portfolio(filename="portfolio.json"):
    portfolio = []

    while True:
        stock_code = input("Enter stock code (e.g., AAPL): ").strip().upper()
        shares = int(input(f"How many shares of {stock_code} did you buy? "))
        purchase_date = input("When did you buy it? (YYYY-MM-DD): ").strip()

        portfolio.append({
            "stock_code": stock_code,
            "shares": shares,
            "purchase_date": purchase_date
        })

        cont = input("Add another stock? (y/n): ").strip().lower()
        if cont != "y":
            break

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(portfolio, f, indent=2)

    print(f"\nPortfolio saved to {filename}")

if __name__ == "__main__":
    create_portfolio()

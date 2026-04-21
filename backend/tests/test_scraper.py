from scraper.fetch_price import get_prices
from scraper.utils import save_prices

print("Running scraper...")

product = "iphone"

prices = get_prices(product)

print("Prices:", prices)

if prices:
    save_prices(prices)
    print("Saved to CSV!")
else:
    print("No prices found")
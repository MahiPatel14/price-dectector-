from scraper.selenium_scraper import get_flipkart_price

url = "https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4"

print("Running scraper...")
price = get_flipkart_price(url)

print("Price:", price)
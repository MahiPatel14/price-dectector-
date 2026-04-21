import requests
from bs4 import BeautifulSoup
import urllib3
import csv
from datetime import datetime

# disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_price(url):
    print("Fetching URL...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, verify=False)
    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    # Flipkart price selector
    price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})

    # fallback
    if price_tag is None:
        print("Primary selector failed, trying backup...")
        price_tag = soup.find("span")

    if price_tag is None:
        print("❌ Price not found")
        return None

    price_text = price_tag.text.strip()
    print("Raw Price:", price_text)

    # detect block
    if "login" in price_text.lower():
        print("❌ Blocked by website (login page detected)")
        return None

    # clean price
    try:
        price_number = int(price_text.replace("₹", "").replace(",", ""))
        return price_number
    except:
        print("Could not convert price")
        return None
import csv
from datetime import datetime
import os

def save_prices(product, prices):
    file_path = "data/raw/price_log.csv"

    # Ensure file exists with header
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "product", "source", "price"])

    # Append clean data
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)

        for source, price in prices.items():
            if isinstance(price, (int, float)):  # ✅ ONLY SAVE VALID PRICES
                writer.writerow([datetime.now(), product, source, price])
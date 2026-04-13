def get_price(url):
    print("Fetching URL...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, verify=False)

    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    # Try multiple selectors (IMPORTANT 🔥)
    price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})

    if price_tag is None:
        print("Primary selector failed, trying backup...")
        price_tag = soup.find("span")

    if price_tag is None:
        print("❌ Price not found (site blocked or structure changed)")
        return None

    price_text = price_tag.text.strip()
    print("Raw Price:", price_text)

    # Clean price
    try:
        price_number = int(price_text.replace("₹", "").replace(",", ""))
        return price_number
    except:
        print("Could not convert price")
        return price_text 
import csv
from datetime import datetime

def save_price(price):
    file_path = "data/raw/price_log.csv"

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), price])
import requests
from bs4 import BeautifulSoup

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # ⚠️ This depends on website
    price = soup.find("span")

    return price.text if price else None


if __name__ == "__main__":
    url = "https://example.com/product"
    print(get_price(url))
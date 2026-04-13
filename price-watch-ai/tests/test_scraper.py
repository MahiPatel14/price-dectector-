from scraper.utils import get_price, save_price

url = "https://www.flipkart.com/hp-15s-metal-intel-core-i3-13th-gen-1315u-8-gb-512-gb-ssd-windows-11-home-15-hr0005tu-thin-light-laptop/p/itmb433fd9435785?pid=COMHBFRJKS4UDSRU&lid=LSTCOMHBFRJKS4UDSRUPUBRZY&marketplace=FLIPKART&BU=CoreElectronics&pageUID=1776070529293"

price = get_price(url)

print("Price:", price)

if price:
    save_price(price)
    print("Saved to CSV!")
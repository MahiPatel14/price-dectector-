import os
import json
from scraper.generic_scraper import fetch_price_generic

def get_prices(product):
    print(f"Running scraper for: {product}")
    prices = {}

    config_path = os.path.join(os.path.dirname(__file__), "sites_config.json")
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return prices

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            sites_config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing sites_config.json: {e}")
            return prices

    for site_name, site_cfg in sites_config.items():
        print(f"Fetching from {site_name}...")
        price = fetch_price_generic(product, site_cfg)
        if price is not None:
            print(f"{site_name}: {price}")
            prices[site_name] = price
        else:
            print(f"{site_name}: Price not found")

    return prices
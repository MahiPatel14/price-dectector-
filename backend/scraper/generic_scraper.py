import json
import os
from typing import Optional
import time

import requests
from bs4 import BeautifulSoup

def _get_driver():
    import os
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Try to use standard configuration
    return webdriver.Chrome(options=options)

def _extract_price_text(text: str) -> Optional[float]:
    if not text:
        return None
    cleaned = text.replace("₹", "").replace("Rs.", "").replace(",", "").replace("$", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None

def fetch_price_generic(product: str, site_cfg: dict) -> Optional[float]:
    query_str = product.replace(" ", "+") if "myntra" not in site_cfg["url_template"] else product.replace(" ", "-")
    url = site_cfg["url_template"].format(query=query_str)
    method = site_cfg.get("method", "requests").lower()
    
    # price_selector can be a comma-separated list of selectors
    selectors = [s.strip() for s in site_cfg["price_selector"].split(",")]

    print(f"  -> Requesting {url} via {method}")

    if method == "requests":
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        try:
            resp = requests.get(url, timeout=10, headers=headers)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    return _extract_price_text(element.get_text())
            return None
        except Exception as e:
            print(f"  -> Requests error: {e}")
            return None
            
    elif method == "selenium":
        driver = None
        try:
            driver = _get_driver()
            driver.get(url)
            
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            wait = WebDriverWait(driver, 10)
            
            for selector in selectors:
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    price = _extract_price_text(element.text)
                    if price is not None:
                        return price
                except:
                    continue
            return None
        except Exception as e:
            print(f"  -> Selenium error: {e}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    return None

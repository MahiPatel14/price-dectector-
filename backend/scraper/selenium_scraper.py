from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_flipkart_price(url):
    print("Opening Flipkart...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--disable-web-security")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        try:
            close_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
            )
            close_btn.click()
            print("Popup closed")
        except:
            print("No popup")

        price_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'₹')]"))
        )

        price_text = price_element.text
        print("Raw price:", price_text)

        price = price_text.replace("₹", "").replace(",", "")
        return float(price)

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        driver.quit()

def get_croma_price(url):

    print("Opening Croma...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".amount"))
        )

        price_text = price_element.text
        print("Raw Croma price:", price_text)

        price = price_text.replace("₹", "").replace(",", "")
        return float(price)

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        driver.quit()        
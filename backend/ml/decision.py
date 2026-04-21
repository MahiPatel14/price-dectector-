def best_price(prices: dict):
    """
    Returns the website with lowest price
    """
    if not prices:
        return None, None

    best_site = min(prices, key=prices.get)
    return best_site, prices[best_site]


def buy_decision(current_price, predicted_price):
    """
    Simple decision logic
    """
    if predicted_price is None:
        return "Not enough data"

    if predicted_price > current_price:
        return "Wait — price may increase "

    elif predicted_price < current_price:
        return "Buy now — price may drop "

    else:
        return "Stable price "

def filter_anomalies(prices: dict) -> tuple[dict, dict]:
    """
    Identifies and removes statistical anomalies (e.g. accessories scraped instead of laptops).
    Returns (clean_prices, anomalies)
    """
    if not prices:
        return {}, {}
        
    prices_list = list(prices.values())
    prices_list.sort()
    
    n = len(prices_list)
    if n % 2 == 1:
        median = prices_list[n//2]
    else:
        median = (prices_list[n//2 - 1] + prices_list[n//2]) / 2.0
        
    clean_prices = {}
    anomalies = {}
    
    for site, p in prices.items():
        if p < (0.5 * median) or p > (2.0 * median):
            anomalies[site] = p
        else:
            clean_prices[site] = p
            
    return clean_prices, anomalies
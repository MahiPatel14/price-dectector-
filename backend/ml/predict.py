import pandas as pd

def predict_next_price(file_path: str, product: str):
    df = pd.read_csv(file_path)

    if "product" in df.columns:
        df = df[df["product"].str.lower() == product.lower()]

    if "price" not in df.columns or len(df) == 0:
        return None

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    
    if len(df) == 0:
        return None

    if len(df) < 3:
        return df["price"].mean()

    # Simple prediction = moving average
    return df["price"].tail(3).mean()

def forecast_next_days(file_path: str, product: str, days: int = 3) -> list[float]:
    """
    Given historical prices, return a list of predicted prices for the next `days` days.
    """
    df = pd.read_csv(file_path)

    if "product" in df.columns:
        df = df[df["product"].str.lower() == product.lower()]

    if "price" not in df.columns or len(df) == 0:
        return []
    
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])

    if len(df) == 0:
        return []
    
    recent_mean = df["price"].tail(3).mean()
    last_price = df["price"].iloc[-1]
    
    if len(df) >= 4:
        trend = last_price - df["price"].tail(4).head(2).mean()
    else:
        trend = 0
        
    trend = trend * 0.5 
    
    forecast = []
    current_pred = recent_mean
    for i in range(days):
        current_pred += (trend / (i+1))
        forecast.append(round(float(current_pred), 2))
        
    return forecast
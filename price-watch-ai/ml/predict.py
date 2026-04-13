import pandas as pd

def predict_next_price(csv_path):
    df = pd.read_csv(csv_path)

    # moving average (last 3 days)
    prediction = df["price"].rolling(3).mean().iloc[-1]

    return prediction
"""
Price Watch AI — FastAPI Backend
Wraps existing scraper + ML modules and exposes REST endpoints
for the Next.js frontend.
"""

import sys
import os

# Ensure the backend directory is on the path so we can import scraper/ml
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from scraper.fetch_price import get_prices
from scraper.utils import save_prices
from ml.predict import predict_next_price, forecast_next_days
from ml.decision import best_price, buy_decision, filter_anomalies

app = FastAPI(title="Price Watch AI API", version="1.0.0")

# ---------------------------------------------------------------------------
# CORS — allow the Next.js dev server (port 3000) to call us
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "price_log.csv")

# ---------------------------------------------------------------------------
# GET /api/search?product=iphone
# ---------------------------------------------------------------------------
@app.get("/api/search")
def search_product(product: str = Query(..., min_length=1)):
    """
    Scrape live prices for *product*, persist them to CSV, and return
    prices + best price + AI prediction + recommendation.
    """
    # 1. Fetch live prices
    prices = get_prices(product)

    # 1.5 Filter out statistical outliers
    prices, anomalies = filter_anomalies(prices)

    if not prices:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch valid prices for that product. Try again or check the scrapers.",
        )

    # 2. Persist to CSV
    save_prices(product, prices)

    # 3. Best price
    best_site, best_value = best_price(prices)

    prediction = None
    forecast_data = {}
    if os.path.exists(DATA_PATH):
        prediction = predict_next_price(DATA_PATH, product)
        if prediction is not None:
            prediction = round(float(prediction), 2)
            
        forecast_list = forecast_next_days(DATA_PATH, product, days=3)
        if len(forecast_list) == 3:
            day3_price = forecast_list[-1]
            drop_percent = 0.0
            if best_value and best_value > 0:
                drop_percent = ((best_value - day3_price) / best_value) * 100
            
            forecast_data = {
                "day1": forecast_list[0],
                "day2": forecast_list[1],
                "day3": forecast_list[2],
                "drop_percent": round(drop_percent, 2)
            }

    # 5. Decision
    decision_text = buy_decision(best_value, prediction) if prediction else None
    
    # Optional enhancement: update decision based on forecast instead
    if forecast_data and forecast_data.get("drop_percent", 0) > 2.0:
        decision_text = f"Buy later – expected to drop by {forecast_data['drop_percent']}% in 3 days."

    # 6. Trend analysis
    trend = None
    if prediction is not None and best_value is not None:
        if prediction < best_value:
            trend = "📉 Price may drop — consider waiting or buying now at the current low."
        elif prediction > best_value:
            trend = "📈 Price may rise — now might be a good time to buy."
        else:
            trend = "➡️ Price is stable — no urgent action needed."

    return {
        "product": product,
        "prices": prices,
        "anomalies": anomalies,         # Explicitly passed ignored prices
        "best_site": best_site,
        "best_value": best_value,
        "lowest_price": best_value,     # Added for explicit clarity
        "prediction": prediction,
        "forecast": forecast_data,      # Added 3-day forecast + drop%
        "decision": decision_text,
        "trend": trend,
    }


# ---------------------------------------------------------------------------
# GET /api/history
# ---------------------------------------------------------------------------
@app.get("/api/history")
def get_history(product: str = Query(..., min_length=1)):
    """
    Return all rows from the price CSV as a JSON array.
    Returns an empty list when no data exists yet.
    """
    if not os.path.exists(DATA_PATH):
        return {"rows": []}

    try:
        df = pd.read_csv(DATA_PATH)
        if "product" in df.columns:
            df = df[df["product"].str.lower() == product.lower()]
        
        # Ensure we only have the expected columns
        # We can drop the product column from the response since the frontend only needs date, source, price
        if set(["date", "source", "price"]).issubset(df.columns):
            df = df[["date", "source", "price"]].copy()
        else:
            return {"rows": []}

        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna()
        return {"rows": df.to_dict(orient="records")}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not read CSV: {exc}")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

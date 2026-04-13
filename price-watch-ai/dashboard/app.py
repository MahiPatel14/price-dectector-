import sys
import os

# -------------------------------
# Fix import path
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from ml.predict import predict_next_price
from ml.decision import make_decision

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(
    page_title="Price Watch AI",
    layout="centered"
)

st.title("Price Watch AI Dashboard")
st.markdown("###  Smart Price Tracking & Prediction System")

# -------------------------------
# Load Data
# -------------------------------
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "price_log.csv")

if not os.path.exists(DATA_PATH):
    st.warning("⚠️ No data found. Run the scraper first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# -------------------------------
# Price Chart
# -------------------------------
st.subheader(" Price History")
st.line_chart(df["price"])

# -------------------------------
# Latest Price
# -------------------------------
current_price = df["price"].iloc[-1]

st.subheader(" Latest Price")
st.write(f"Latest recorded price is **₹{current_price}**")

# -------------------------------
# Prediction
# -------------------------------
prediction = predict_next_price(DATA_PATH)

st.subheader(" AI Insights")

col1, col2 = st.columns(2)

with col1:
    st.metric(" Current Price", current_price)

with col2:
    st.metric(" Predicted Price", round(prediction, 2))

# -------------------------------
# Price Change Indicator
# -------------------------------
price_diff = prediction - current_price

st.metric(
    label="Expected Change",
    value=round(price_diff, 2),
    delta=round(price_diff, 2)
)

# -------------------------------
# Decision
# -------------------------------
st.subheader(" Recommendation")

decision = make_decision(current_price, prediction)

if "Buy" in decision:
    st.success(decision)
else:
    st.warning(decision)

# -------------------------------
# Insight Explanation
# -------------------------------
st.subheader("Insight")

if prediction > current_price:
    st.write("The model predicts an increase in price. You may consider waiting.")
else:
    st.write("The model predicts a stable or decreasing trend. It might be a good time to buy.")

# -------------------------------
# Raw Data
# -------------------------------
st.subheader("Raw Data")
st.dataframe(df)
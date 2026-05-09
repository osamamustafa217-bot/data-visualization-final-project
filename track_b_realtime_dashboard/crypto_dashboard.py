import random
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# ------------------------------------------------------------
# Track B - Real-Time Data Visualization
# Project: Live Crypto Monitoring Dashboard
# Data Source: CoinGecko API with demo-safe fallback
# ------------------------------------------------------------

st.set_page_config(
    page_title="Live Crypto Monitoring Dashboard",
    page_icon="📈",
    layout="wide",
)

st.sidebar.title("Dashboard Settings")

coin_id = st.sidebar.text_input("Coin ID", value="bitcoin")
currency = st.sidebar.text_input("Currency", value="usd")

refresh_interval = st.sidebar.slider(
    "Refresh interval (seconds)",
    min_value=10,
    max_value=60,
    value=25,
)

alert_threshold = st.sidebar.slider(
    "Alert threshold for window change (%)",
    min_value=0.1,
    max_value=10.0,
    value=0.2,
)

auto_refresh = st.sidebar.checkbox(
    "Auto refresh dashboard",
    value=False
)

use_demo_fallback = st.sidebar.checkbox(
    "Use demo fallback if API fails",
    value=True
)

st.sidebar.info(
    "The dashboard uses CoinGecko API when available. "
    "If the API is blocked, demo fallback keeps the dashboard working."
)


# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------

if "price_history" not in st.session_state:
    st.session_state.price_history = []

if "base_price" not in st.session_state:
    st.session_state.base_price = 65000.0


# ------------------------------------------------------------
# API Function
# ------------------------------------------------------------

def fetch_crypto_price(coin_id_value, currency_value):
    """
    Fetch live cryptocurrency price from CoinGecko API.

    Returns:
        current_price, change_24h, connection_status
    """
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id_value,
        "vs_currencies": currency_value,
        "include_24hr_change": "true",
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()

        data = response.json()

        if coin_id_value not in data:
            raise ValueError("Coin ID not found in API response.")

        current_price = float(data[coin_id_value][currency_value])
        change_key = f"{currency_value}_24h_change"
        change_24h = float(data[coin_id_value].get(change_key, 0.0))

        return round(current_price, 2), round(change_24h, 2), "Live API"

    except Exception:
        if not use_demo_fallback:
            raise

        # Demo-safe fallback
        price_change = random.uniform(-250, 250)
        st.session_state.base_price += price_change

        current_price = round(st.session_state.base_price, 2)
        change_24h = round(random.uniform(-4, 4), 2)

        return current_price, change_24h, "Demo Fallback"


# ------------------------------------------------------------
# Main Dashboard
# ------------------------------------------------------------

st.title("Live Crypto Monitoring Dashboard")

st.write(
    "This dashboard monitors cryptocurrency price movement using a live API when available. "
    "It also includes a demo-safe fallback to prevent presentation failure if the API is blocked."
)

try:
    current_price, change_24h, connection_status = fetch_crypto_price(
        coin_id.lower().strip(),
        currency.lower().strip()
    )
except Exception as error:
    st.error(f"API connection failed: {error}")
    st.stop()

timestamp = datetime.now().strftime("%H:%M:%S")

st.session_state.price_history.append(
    {
        "Time": timestamp,
        "Coin": coin_id.lower().strip(),
        "Currency": currency.upper().strip(),
        "Price": current_price,
    }
)

# Sliding window: keep last 30 readings
st.session_state.price_history = st.session_state.price_history[-30:]

df = pd.DataFrame(st.session_state.price_history)

if len(df) > 1:
    first_price = df["Price"].iloc[0]
    last_price = df["Price"].iloc[-1]
    window_change = ((last_price - first_price) / first_price) * 100
else:
    window_change = 0.0


# ------------------------------------------------------------
# Metrics
# ------------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Current Price", f"{current_price:,.2f} {currency.upper()}")
col2.metric("24h Change", f"{change_24h:.2f}%")
col3.metric("Window Change", f"{window_change:.2f}%")
col4.metric("Connection", connection_status)
col5.metric("Last Updated", timestamp)


# ------------------------------------------------------------
# Alert Logic
# ------------------------------------------------------------

if abs(window_change) >= alert_threshold:
    st.error(
        f"Alert: price movement exceeded the selected threshold "
        f"({window_change:.2f}% / {alert_threshold:.2f}%)."
    )
else:
    st.success("Status: price movement is within the normal range.")


# ------------------------------------------------------------
# Sliding Window Chart
# ------------------------------------------------------------

fig = px.line(
    df,
    x="Time",
    y="Price",
    markers=True,
    title=f"{coin_id.capitalize()} Price Movement ({currency.upper()})",
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title=f"Price ({currency.upper()})",
    yaxis_fixedrange=False,
)

st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# Recent Data Table
# ------------------------------------------------------------

with st.expander("Recent Price Data", expanded=False):
    st.dataframe(df, use_container_width=True)


# ------------------------------------------------------------
# Design Notes
# ------------------------------------------------------------

with st.expander("Design Notes", expanded=False):
    st.write(
        """
        - Data Source: CoinGecko API.
        - Ingestion Method: REST polling.
        - Refresh Rate: User-controlled interval from 10 to 60 seconds.
        - Sliding Window: The chart keeps the last 30 data points.
        - Alert Logic: A warning appears when the window change exceeds the selected threshold.
        - Latency Indicator: The dashboard displays the latest update timestamp.
        - Demo Fallback: If the API is blocked, simulated data keeps the dashboard available for presentation.
        """
    )


# ------------------------------------------------------------
# Auto Refresh
# ------------------------------------------------------------

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
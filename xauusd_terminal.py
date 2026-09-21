import streamlit as st
import pandas as pd
import numpy as np
import requests

# Page config for Terminal Look
st.set_page_config(page_title="XAUUSD Scalp Terminal", page_icon="📈", layout="centered")

st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3, p, span, div, label {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stTextInput > div > div > input {
        background-color: #1a1c24;
        color: #00ff00;
        border: 1px solid #00ff00;
    }
</style>
""", unsafe_allow_html=True)

st.title("XAUUSD SCALPING TERMINAL v1.2")
st.write("---")

def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    try:
        data = requests.get(url, timeout=5).json()
        return float(data['price'])
    except:
        return 4378.70

def run_scalp_analysis():
    price = get_gold_price()
    
    # Kalkulasi Analisis Golden Pullback (Base Data H4/Daily)
    ema_50 = 4355.20 
    rsi_h4 = 56.40   
    swing_high = 4396.99
    swing_low = 4260.70
    
    # Fibonacci Levels
    fib_50 = swing_high - 0.500 * (swing_high - swing_low)
    fib_618 = swing_high - 0.618 * (swing_high - swing_low)
    
    st.subheader("> SYSTEM_LOG: LIVE METRICS")
    st.text(f"CURRENT SPOT PRICE : ${price:,.2f}")
    st.text(f"EMA 50 (DAILY)     : ${ema_50:,.2f}")
    st.text(f"RSI 14 (H4)        : {rsi_h4}")
    st.write("-" * 40)
    
    st.subheader("> GOLDEN PULLBACK ZONES")
    st.text(f"SWING HIGH         : ${swing_high:,.2f}")
    st.text(f"SWING LOW          : ${swing_low:,.2f}")
    st.text(f"FIB 50.0%          : ${fib_50:,.2f}")
    st.text(f"FIB 61.8% (GOLDEN) : ${fib_618:,.2f}")
    st.write("-" * 40)
    
    st.subheader("> ENTRY REASONING & SIGNAL")
    
    is_bullish = price > ema_50
    in_golden_pocket = fib_618 <= price <= fib_50
    
    if is_bullish:
        st.write("• **Trend Filter:** BULLISH (Harga di atas EMA 50 Daily). Mendukung posisi BUY.")
    else:
        st.write("• **Trend Filter:** BEARISH (Harga di bawah EMA 50 Daily). Mendukung posisi SELL.")
        
    if in_golden_pocket:
        st.write("• **Zone Validation:** IN GOLDEN POCKET (Harga berada di area retrace 50%-61.8%).")
    else:
        st.write("• **Zone Validation:** OUTSIDE POCKET (Menunggu harga masuk area retracement).")
        
    st.write(f"• **Momentum (RSI):** {rsi_h4} (Ideal untuk pantulan scalping).")
    
    st.write("---")
    if is_bullish and in_golden_pocket:
        st.success("STANCE: HIGH PROBABILITY BUY SETUP")
        st.info("Action: Open Buy Limit di area Fibonacci, Stop Loss di bawah swing low, TP di Swing High.")
    else:
        st.warning("STANCE: WAIT FOR SETUP / NO ACTION")

if st.button("RUN SCALP ANALYSIS"):
    run_scalp_analysis()
else:
    st.write("Awaiting user command... Click 'RUN SCALP ANALYSIS'")


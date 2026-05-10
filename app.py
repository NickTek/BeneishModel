import streamlit as st
from utils.parsers import get_financial_data
from utils.beneish import calculate_beneish_score

st.set_page_config(page_title="Beneish M-Score", layout="wide")

st.title("📊 Beneish M-Score Analyzer (Stable yfinance version)")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT, TCS.NS)")

if st.button("Calculate M-Score"):

    if not ticker:
        st.error("Please enter a ticker")
    else:
        try:
            bs, pl, cy, py = get_financial_data(ticker)

            result = calculate_beneish_score(bs, pl, cy, py)

            st.subheader("📌 M-Score")
            st.metric("Score", round(result["M_SCORE"], 3))

            if result["M_SCORE"] > -2.22:
                st.error("⚠️ Possible earnings manipulation")
            else:
                st.success("✔ Low manipulation risk")

            st.subheader("📊 Ratios")
            st.json(result)

            st.subheader("🏦 Balance Sheet")
            st.dataframe(bs)

            st.subheader("📈 Income Statement")
            st.dataframe(pl)

        except Exception as e:
            st.exception(e)

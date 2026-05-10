import streamlit as st
from utils.parsers import get_financial_data
from utils.beneish import calculate_beneish_score

st.set_page_config(page_title="Beneish M-Score", layout="wide")

st.title("📊 Beneish M-Score Financial Manipulation Detector")

st.markdown(
    """
Enter a stock ticker to calculate the Beneish M-Score.

Examples:
- AAPL
- MSFT
- TCS.NS
- INFY.NS
"""
)

ticker = st.text_input("Enter ticker")

if st.button("Calculate"):

    if ticker.strip() == "":
        st.error("Please enter a ticker.")
    else:
        try:
            bs, pl, cy, py = get_financial_data(ticker)

            result = calculate_beneish_score(bs, pl, cy, py)

            st.subheader("📌 M-Score")

            mscore = result["M_SCORE"]

            st.metric("Score", round(mscore, 3))

            if mscore > -2.22:
                st.error("⚠️ Possible earnings manipulation risk")
            else:
                st.success("✔ Low manipulation risk")

            st.subheader("📊 Ratios")
            st.json(result)

        except Exception as e:
            st.exception(e)

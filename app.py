import streamlit as st
from utils.parsers import get_financial_data
from utils.beneish import calculate_beneish_score

st.set_page_config(page_title="Beneish M-Score", layout="wide")

st.title("Beneish M-Score Calculator")

st.markdown(
    """
   
    A Beneish M-socre is a mathematical model that uses 8 financial metrics to arrive at a calculated score which can determine whether or not a company has manipulated its financial statements.
    
    A M-socre grearter than -2.22 implies that the financial statements have been manipulated.
    
    Read more about this at: https://resource.cdn.icai.org/59639cajournal-may2020-15.pdf [The Chartered Accountant, May 2020]
    
    This is code written in Python that takes a ticker code from Yahoo finance as input and returns the M-socre.
    """)

st.markdown(
        """
    Enter a stock ticker to calculate the Beneish M-Score. Refer to Yahoo Finance to find ticker codes
    
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
            bs, pl, cf, cy, py = get_financial_data(ticker)

            result = calculate_beneish_score(bs, pl, cf, cy, py)

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

    st.markdown(
    """
    Beneish M-Score
    A Beneish M-socre is a mathematical model that uses 8 financial metrics to arrive at a calculated score which can determine whether or not a company has manipulated its financial statements.
    
    A M-socre grearter than -2.22 implies that the financial statements have been manipulated.
    
    Read more about this at: https://resource.cdn.icai.org/59639cajournal-may2020-15.pdf [The Chartered Accountant, May 2020]
    
    About this code
    This is code written in Python that takes a ticker code from Yahoo finance as input and returns the M-socre.
    """)

import streamlit as st

st.title("Beneish M-Score Financial Manipulation Detector")

st.markdown(
    """
Paste a Yahoo Finance or Moneycontrol financial statement URL.

Examples:
- https://finance.yahoo.com/quote/AAPL/financials
- https://www.moneycontrol.com/financials/tcs/profit-lossVI/TCS
"""
)

url = st.text_input("Financial Statement URL")

if st.button("Calculate Beneish Score"):
    if not url:
        st.error("Please enter a valid URL")
    else:
        try:
            with st.spinner("Fetching financial statements..."):
                bs_df, pl_df, current_year, previous_year = get_financial_data(url)

            with st.spinner("Calculating Beneish score..."):
                result = calculate_beneish_score(
                    bs_df,
                    pl_df,
                    current_year,
                    previous_year,
                )

            st.success("Calculation completed")

            st.subheader("Beneish M-Score")
            st.metric("M-Score", round(result["M_SCORE"], 3))

            if result["M_SCORE"] > -2.22:
                st.error(
                    "Potential earnings manipulation detected (M-Score > -2.22)"
                )
            else:
                st.success(
                    "Low probability of earnings manipulation (M-Score <= -2.22)"
                )

            st.subheader("Component Ratios")
            st.json(result)

            st.subheader("Balance Sheet Data")
            st.dataframe(bs_df)

            st.subheader("Profit & Loss Data")
            st.dataframe(pl_df)

        except Exception as e:
            st.exception(e)

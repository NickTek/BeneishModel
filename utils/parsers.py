import yfinance as yf
import pandas as pd


def get_financial_data(ticker: str):
    stock = yf.Ticker(ticker)

    income = stock.financials
    balance = stock.balance_sheet

    if income.empty or balance.empty:
        raise ValueError("No financial data found for ticker")

    # Ensure enough columns (years)
    years = list(income.columns)

    if len(years) < 2:
        raise ValueError("Need at least 2 years of data")

    current_year = years[0]
    previous_year = years[1]

    return balance, income, current_year, previous_year


# ---------------------------
# SAFE LOOKUP FUNCTION
# ---------------------------
def safe_get(df, possible_names, col):
    for name in possible_names:
        if name in df.index:
            return df.loc[name, col]
    return 0

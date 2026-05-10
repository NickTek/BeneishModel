import yfinance as yf
import pandas as pd
import numpy as np


def get_financial_data(ticker: str):
    stock = yf.Ticker(ticker)

    income = stock.financials
    balance = stock.balance_sheet

    if income.empty or balance.empty:
        raise ValueError("No financial data found for ticker")

    years = list(income.columns)

    if len(years) < 2:
        raise ValueError("Need at least 2 years of data")

    return balance, income, years[0], years[1]


# ---------------- SAFE LOOKUP ----------------
def safe_get(df, possible_names, col):
    for name in possible_names:
        if name in df.index:
            val = df.loc[name, col]
            if pd.notna(val):
                return float(val)
    return np.nan


def clean(x):
    return 0 if pd.isna(x) else float(x)

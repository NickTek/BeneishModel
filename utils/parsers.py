import yfinance as yf
import pandas as pd
import numpy as np


def get_financial_data(ticker):

    stock = yf.Ticker(ticker)

    income = stock.financials
    balance = stock.balance_sheet

    if income.empty:
        raise ValueError("Income statement not found")

    if balance.empty:
        raise ValueError("Balance sheet not found")

    years = list(income.columns)

    if len(years) < 2:
        raise ValueError("Need at least 2 years of financial data")

    current_year = years[0]
    previous_year = years[1]

    return balance, income, current_year, previous_year


def safe_get(df, possible_names, col):

    for name in possible_names:

        if name in df.index:

            value = df.loc[name, col]

            if pd.notna(value):
                return float(value)

    return np.nan


def clean_ratio(x):

    if pd.isna(x):
        return 1.0

    if np.isinf(x):
        return 1.0

    return float(x)

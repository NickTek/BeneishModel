import yfinance as yf
import pandas as pd


def get_financial_data(ticker: str):
    stock = yf.Ticker(ticker)

    # Financial statements
    income = stock.financials
    balance = stock.balance_sheet
    cashflow = stock.cashflow

    if income.empty or balance.empty:
        raise ValueError("No financial data found for ticker")

    # Align years (columns)
    years = list(income.columns)

    if len(years) < 2:
        raise ValueError("Need at least 2 years of data")

    current_year = years[0]
    previous_year = years[1]

    return balance, income, current_year, previous_year

import yfinance as yf


def get_yahoo_financials(ticker):

    company = yf.Ticker(ticker)

    income_statement = company.financials
    balance_sheet = company.balance_sheet
    cashflow = company.cashflow

    income_statement = income_statement.fillna(0)
    balance_sheet = balance_sheet.fillna(0)
    cashflow = cashflow.fillna(0)

    income_statement.columns = [col.strftime('%Y') for col in income_statement.columns]
    balance_sheet.columns = [col.strftime('%Y') for col in balance_sheet.columns]
    cashflow.columns = [col.strftime('%Y') for col in cashflow.columns]

    return income_statement, balance_sheet, cashflow

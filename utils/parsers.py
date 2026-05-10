import pandas as pd


def get_financial_data(url):
    if "moneycontrol.com" in url:
        return parse_moneycontrol(url)

    if "yahoo.com" in url:
        return parse_yahoo_finance(url)

    raise ValueError("Unsupported URL")


def parse_moneycontrol(url):
    tables = pd.read_html(url)

    pl_df = tables[0]
    bs_df = tables[1]

    years = list(pl_df.columns)
    current_year = years[0]
    previous_year = years[1]

    return bs_df, pl_df, current_year, previous_year


def parse_yahoo_finance(url):
    raise NotImplementedError("Yahoo Finance parsing not implemented yet")

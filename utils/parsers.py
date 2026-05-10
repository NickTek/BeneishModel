import pandas as pd

import pandas as pd

def get_financial_data(url):
    if "moneycontrol.com" in url:
        return parse_moneycontrol(url)

    if "yahoo.com" in url:
        return parse_yahoo_finance(url)

    raise ValueError("Unsupported URL")

def parse_moneycontrol(url):
    tables = pd.read_html(url)

    if len(tables) < 2:
        raise ValueError("Unable to parse Moneycontrol financial tables")

    # Adjust table indexes if necessary
    pl_df = tables[0]
    bs_df = tables[1]

    # Cleanup
    pl_df = clean_dataframe(pl_df)
    bs_df = clean_dataframe(bs_df)

    years = list(pl_df.columns)

    current_year = years[0]
    previous_year = years[1]

    return bs_df, pl_df, current_year, previous_year


# ---------------------------------------------------------------------
# YAHOO FINANCE PARSER
# ---------------------------------------------------------------------


def parse_yahoo_finance(url):
    raise NotImplementedError(
        "Yahoo Finance financial statements are dynamically rendered. "
        "Use yfinance API or Playwright for production implementation."
    )


# ---------------------------------------------------------------------
# CLEANUP HELPERS
# ---------------------------------------------------------------------


def clean_dataframe(df):
    df.columns = df.iloc[0]
    df = df[1:]

    first_col = df.columns[0]

    df = df.rename(columns={first_col: "LineItem"})
    df = df.set_index("LineItem")

    # Convert all values to numeric
    for col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(',', '')
            .str.replace('--', '0')
        )

        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df

def calculate_beneish_score(BS, PL, CY, PY):

    # DSRI
    DSR_CY = BS.loc['Accounts Receivable', CY] / PL.loc['Total Revenue', CY]
    DSR_PY = BS.loc['Accounts Receivable', PY] / PL.loc['Total Revenue', PY]
    DSRI = DSR_CY / DSR_PY

    # GMI
    GM_CY = (PL.loc['Total Revenue', CY] - PL.loc['Cost Of Revenue', CY]) / PL.loc['Total Revenue', CY]
    GM_PY = (PL.loc['Total Revenue', PY] - PL.loc['Cost Of Revenue', PY]) / PL.loc['Total Revenue', PY]
    GMI = GM_PY / GM_CY

    # AQI
    AQI = (
        (BS.loc['Total Assets', CY] - BS.loc['Current Assets', CY]) / BS.loc['Total Assets', CY]
    ) / (
        (BS.loc['Total Assets', PY] - BS.loc['Current Assets', PY]) / BS.loc['Total Assets', PY]
    )

    # SGI
    SGI = PL.loc['Total Revenue', CY] / PL.loc['Total Revenue', PY]

    # LVGI
    LVGI = (
        (BS.loc['Total Liab', CY] / BS.loc['Total Assets', CY]) /
        (BS.loc['Total Liab', PY] / BS.loc['Total Assets', PY])
    )

    # TATA (simplified)
    TATA = (
        (BS.loc['Total Current Assets', CY] - BS.loc['Total Current Liab', CY]) -
        (BS.loc['Total Current Assets', PY] - BS.loc['Total Current Liab', PY])
    ) / BS.loc['Total Assets', CY]

    # M-Score
    M = (
        -4.84
        + 0.92 * DSRI
        + 0.528 * GMI
        + 0.404 * AQI
        + 0.892 * SGI
        - 0.172 * LVGI
        + 4.679 * TATA
    )

    return {
        "DSRI": DSRI,
        "GMI": GMI,
        "AQI": AQI,
        "SGI": SGI,
        "LVGI": LVGI,
        "TATA": TATA,
        "M_SCORE": M
    }

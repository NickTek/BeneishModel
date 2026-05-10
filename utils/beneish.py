import pandas as pd
    LV_PY = (
        (
            BS.loc['Total Non-Current Liabilities', PY]
            + BS.loc['Total Current Liabilities', PY]
        )
        / BS.loc['Total Assets', PY]
    )

    LVGI = LV_CY / LV_PY

    # Total Accruals to Total Assets (TATA)
    Change_WC = (
        (BS.loc['Total Current Assets', CY] - BS.loc['Total Current Liabilities', CY])
        -
        (BS.loc['Total Current Assets', PY] - BS.loc['Total Current Liabilities', PY])
    )

    Change_Cash = (
        BS.loc['Cash And Cash Equivalents', CY]
        - BS.loc['Cash And Cash Equivalents', PY]
    )

    TATA = (
        Change_WC
        - Change_Cash
        - PL.loc['Depreciation And Amortisation Expenses', CY]
    ) / BS.loc['Total Assets', CY]

    # Beneish M-Score
    M = (
        -4.84
        + 0.92 * DSRI
        + 0.528 * GMI
        + 0.404 * AQI
        + 0.892 * SGI
        + 0.115 * DEPI
        - 0.172 * SGAI
        + 4.679 * TATA
        - 0.327 * LVGI
    )

    return {
        "DSRI": float(DSRI),
        "GMI": float(GMI),
        "AQI": float(AQI),
        "SGI": float(SGI),
        "DEPI": float(DEPI),
        "SGAI": float(SGAI),
        "LVGI": float(LVGI),
        "TATA": float(TATA),
        "M_SCORE": float(M),
    }

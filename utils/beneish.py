import pandas as pd
    ]

    cfo_cy = safe_get(CF, cfo_names, CY)
    net_income_cy = safe_get(PL, income_names, CY)

    TATA = sdiv(
        (net_income_cy - cfo_cy),
        ta_cy
    )

    # ==================================================
    # CLEAN VALUES
    # ==================================================

    DSRI = clean_ratio(DSRI)
    GMI = clean_ratio(GMI)
    AQI = clean_ratio(AQI)
    SGI = clean_ratio(SGI)
    DEPI = clean_ratio(DEPI)
    SGAI = clean_ratio(SGAI)
    LVGI = clean_ratio(LVGI)
    TATA = clean_ratio(TATA, neutral=0.0)

    # ==================================================
    # FINAL SCORE
    # ==================================================

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
        "DSRI": round(DSRI, 4),
        "GMI": round(GMI, 4),
        "AQI": round(AQI, 4),
        "SGI": round(SGI, 4),
        "DEPI": round(DEPI, 4),
        "SGAI": round(SGAI, 4),
        "LVGI": round(LVGI, 4),
        "TATA": round(TATA, 4),
        "M_SCORE": round(M, 4)
    }

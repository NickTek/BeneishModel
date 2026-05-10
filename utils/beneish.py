import pandas as pd
from utils.parsers import safe_get, clean_ratio


def calculate_beneish_score(BS, PL, CY, PY):

    # ---------------- Revenue ----------------

    revenue_names = [
        "Total Revenue",
        "Operating Revenue",
        "Revenue"
    ]

    revenue_cy = safe_get(PL, revenue_names, CY)
    revenue_py = safe_get(PL, revenue_names, PY)

    # ---------------- DSRI ----------------

    ar_names = [
        "Accounts Receivable",
        "Net Receivables"
    ]

    ar_cy = safe_get(BS, ar_names, CY)
    ar_py = safe_get(BS, ar_names, PY)

    DSRI = (ar_cy / revenue_cy) / ((ar_py / revenue_py) + 1e-9)

    # ---------------- GMI ----------------

    cost_names = [
        "Cost Of Revenue",
        "Cost Of Goods Sold"
    ]

    cost_cy = safe_get(PL, cost_names, CY)
    cost_py = safe_get(PL, cost_names, PY)

    gm_cy = (revenue_cy - cost_cy) / revenue_cy
    gm_py = (revenue_py - cost_py) / revenue_py

    GMI = gm_py / (gm_cy + 1e-9)

    # ---------------- AQI ----------------

    current_asset_names = [
        "Total Current Assets"
    ]

    total_asset_names = [
        "Total Assets"
    ]

    ca_cy = safe_get(BS, current_asset_names, CY)
    ca_py = safe_get(BS, current_asset_names, PY)

    ta_cy = safe_get(BS, total_asset_names, CY)
    ta_py = safe_get(BS, total_asset_names, PY)

    aqi_num = (ta_cy - ca_cy) / (ta_cy + 1e-9)
    aqi_den = (ta_py - ca_py) / (ta_py + 1e-9)

    AQI = aqi_num / (aqi_den + 1e-9)

    # ---------------- SGI ----------------

    SGI = revenue_cy / (revenue_py + 1e-9)

    # ---------------- DEPI ----------------

    dep_names = [
        "Depreciation",
        "Depreciation & Amortization"
    ]

    dep_cy = safe_get(PL, dep_names, CY)
    dep_py = safe_get(PL, dep_names, PY)

    if pd.isna(dep_cy) or pd.isna(dep_py):
        DEPI = 1.0
    else:
        DEPI = (
            dep_py / (dep_py + ta_py + 1e-9)
        ) / (
            dep_cy / (dep_cy + ta_cy + 1e-9)
        )

    # ---------------- SGAI ----------------

    sga_names = [
        "Operating Expense",
        "Operating Expenses",
        "Other Expenses"
    ]

    sga_cy = safe_get(PL, sga_names, CY)
    sga_py = safe_get(PL, sga_names, PY)

    if pd.isna(sga_cy) or pd.isna(sga_py):
        SGAI = 1.0
    else:
        SGAI = (
            sga_cy / revenue_cy
        ) / (
            (sga_py / revenue_py) + 1e-9
        )

    # ---------------- LVGI ----------------

    liab_names = [
        "Total Liab",
        "Total Liabilities",
        "Total Liabilities Net Minority Interest"
    ]

    liab_cy = safe_get(BS, liab_names, CY)
    liab_py = safe_get(BS, liab_names, PY)

    LVGI = (
        liab_cy / (ta_cy + 1e-9)
    ) / (
        (liab_py / (ta_py + 1e-9)) + 1e-9
    )

    # ---------------- TATA ----------------

    current_liab_names = [
        "Total Current Liabilities"
    ]

    wc_cy = (
        safe_get(BS, current_asset_names, CY)
        - safe_get(BS, current_liab_names, CY)
    )

    wc_py = (
        safe_get(BS, current_asset_names, PY)
        - safe_get(BS, current_liab_names, PY)
    )

    TATA = (wc_cy - wc_py) / (ta_cy + 1e-9)

    # ---------------- CLEAN RATIOS ----------------

    DSRI = clean_ratio(DSRI)
    GMI = clean_ratio(GMI)
    AQI = clean_ratio(AQI)
    SGI = clean_ratio(SGI)
    DEPI = clean_ratio(DEPI)
    SGAI = clean_ratio(SGAI)
    LVGI = clean_ratio(LVGI)
    TATA = 0 if pd.isna(TATA) else float(TATA)

    # ---------------- FINAL SCORE ----------------

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
        "M_SCORE": round(M, 4),
    }

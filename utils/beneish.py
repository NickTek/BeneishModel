import pandas as pd
from utils.parsers import safe_get, clean_ratio


def sdiv(a, b):

    if pd.isna(a) or pd.isna(b):
        return pd.NA

    if b == 0:
        return pd.NA

    return a / b


def calculate_beneish_score(BS, PL, CF, CY, PY):

    # =========================
    # Revenue
    # =========================

    revenue_names = [
        "Total Revenue",
        "Operating Revenue",
        "Revenue"
    ]

    revenue_cy = safe_get(PL, revenue_names, CY)
    revenue_py = safe_get(PL, revenue_names, PY)

    # =========================
    # Receivables
    # =========================

    receivable_names = [
        "Accounts Receivable",
        "Net Receivables",
        "Receivables"
    ]

    ar_cy = safe_get(BS, receivable_names, CY)
    ar_py = safe_get(BS, receivable_names, PY)

    DSRI = sdiv(
        sdiv(ar_cy, revenue_cy),
        sdiv(ar_py, revenue_py)
    )

    # =========================
    # Gross Margin Index
    # =========================

    cost_names = [
        "Cost Of Revenue",
        "Cost Of Goods Sold"
    ]

    cost_cy = safe_get(PL, cost_names, CY)
    cost_py = safe_get(PL, cost_names, PY)

    gm_cy = sdiv((revenue_cy - cost_cy), revenue_cy)
    gm_py = sdiv((revenue_py - cost_py), revenue_py)

    GMI = sdiv(gm_py, gm_cy)

    # =========================
    # Asset Quality Index
    # =========================

    current_asset_names = [
        "Current Assets",
        "Total Current Assets"
    ]

    total_asset_names = [
        "Total Assets"
    ]

    ppe_names = [
        "Net PPE",
        "Property Plant Equipment",
        "Gross PPE"
    ]

    ca_cy = safe_get(BS, current_asset_names, CY)
    ca_py = safe_get(BS, current_asset_names, PY)

    ta_cy = safe_get(BS, total_asset_names, CY)
    ta_py = safe_get(BS, total_asset_names, PY)

    ppe_cy = safe_get(BS, ppe_names, CY)
    ppe_py = safe_get(BS, ppe_names, PY)

    aqi_num = 1 - sdiv((ca_cy + ppe_cy), ta_cy)
    aqi_den = 1 - sdiv((ca_py + ppe_py), ta_py)

    AQI = sdiv(aqi_num, aqi_den)

    # =========================
    # Sales Growth Index
    # =========================

    SGI = sdiv(revenue_cy, revenue_py)

    # =========================
    # Depreciation Index
    # =========================

    dep_names = [
        "Depreciation",
        "Depreciation & Amortization",
        "Depreciation And Amortization"
    ]

    dep_cy = safe_get(CF, dep_names, CY)
    dep_py = safe_get(CF, dep_names, PY)

    dep_rate_cy = sdiv(dep_cy, (dep_cy + ppe_cy))
    dep_rate_py = sdiv(dep_py, (dep_py + ppe_py))

    DEPI = sdiv(dep_rate_py, dep_rate_cy)

    # =========================
    # SGAI
    # =========================

    sga_names = [
        "Selling General Administrative",
        "Operating Expense",
        "Operating Expenses"
    ]

    sga_cy = safe_get(PL, sga_names, CY)
    sga_py = safe_get(PL, sga_names, PY)

    SGAI = sdiv(
        sdiv(sga_cy, revenue_cy),
        sdiv(sga_py, revenue_py)
    )

    # =========================
    # LVGI
    # =========================

    liability_names = [
        "Total Liabilities Net Minority Interest",
        "Total Liab",
        "Total Liabilities"
    ]

    liab_cy = safe_get(BS, liability_names, CY)
    liab_py = safe_get(BS, liability_names, PY)

    LVGI = sdiv(
        sdiv(liab_cy, ta_cy),
        sdiv(liab_py, ta_py)
    )

    # =========================
    # TATA
    # =========================

    cfo_names = [
        "Operating Cash Flow",
        "Cash Flow From Continuing Operating Activities",
        "Net Cash Provided By Operating Activities"
    ]

    income_names = [
        "Net Income",
        "Net Income Common Stockholders"
    ]

    cfo_cy = safe_get(CF, cfo_names, CY)
    net_income_cy = safe_get(PL, income_names, CY)

    TATA = sdiv(
        (net_income_cy - cfo_cy),
        ta_cy
    )

    # =========================
    # CLEAN VALUES
    # =========================

    DSRI = clean_ratio(DSRI)
    GMI = clean_ratio(GMI)
    AQI = clean_ratio(AQI)
    SGI = clean_ratio(SGI)
    DEPI = clean_ratio(DEPI)
    SGAI = clean_ratio(SGAI)
    LVGI = clean_ratio(LVGI)
    TATA = clean_ratio(TATA, neutral=0.0)

    # =========================
    # Final M Score
    # =========================

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

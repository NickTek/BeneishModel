import numpy as np
import pandas as pd
from utils.parsers import safe_get


def calculate_beneish_score(BS, PL, CY, PY):

    # ---------------- REVENUE ----------------
    revenue_names = ["Total Revenue", "Operating Revenue"]
    revenue_cy = safe_get(PL, revenue_names, CY)
    revenue_py = safe_get(PL, revenue_names, PY)

    # fallback safety
    revenue_cy = revenue_cy if not pd.isna(revenue_cy) else 1
    revenue_py = revenue_py if not pd.isna(revenue_py) else 1

    # ---------------- DSRI ----------------
    ar_names = ["Accounts Receivable", "Net Receivables"]
    ar_cy = safe_get(BS, ar_names, CY)
    ar_py = safe_get(BS, ar_names, PY)

    DSRI = (ar_cy / revenue_cy) / (ar_py / revenue_py + 1e-9)

    # ---------------- GMI ----------------
    cost_names = ["Cost Of Revenue", "Cost Of Goods Sold"]
    cost_cy = safe_get(PL, cost_names, CY)
    cost_py = safe_get(PL, cost_names, PY)

    gm_cy = (revenue_cy - cost_cy) / revenue_cy
    gm_py = (revenue_py - cost_py) / revenue_py

    GMI = gm_py / (gm_cy + 1e-9)

    # ---------------- AQI ----------------
    ca = safe_get(BS, ["Total Current Assets"], CY)
    ca_py = safe_get(BS, ["Total Current Assets"], PY)
    ta = safe_get(BS, ["Total Assets"], CY)
    ta_py = safe_get(BS, ["Total Assets"], PY)

    AQI = ((ta - ca) / ta) / ((ta_py - ca_py) / ta_py + 1e-9)

    # ---------------- SGI ----------------
    SGI = revenue_cy / (revenue_py + 1e-9)

    # ---------------- DEPI (FIXED) ----------------
    dep_names = ["Depreciation & Amortization", "Depreciation"]
    dep_cy = safe_get(PL, dep_names, CY)
    dep_py = safe_get(PL, dep_names, PY)

    if pd.isna(dep_cy) or pd.isna(dep_py):
        DEPI = 1.0
    else:
        DEPI = (dep_py / (dep_py + ta_py + 1e-9)) / (dep_cy / (dep_cy + ta + 1e-9))

    # ---------------- SGAI (FIXED) ----------------
    sga_names = ["Operating Expense", "Operating Expenses", "Other Expenses"]
    sga_cy = safe_get(PL, sga_names, CY)
    sga_py = safe_get(PL, sga_names, PY)

    if pd.isna(sga_cy) or pd.isna(sga_py):
        SGAI = 1.0
    else:
        SGAI = (sga_cy / revenue_cy) / (sga_py / revenue_py + 1e-9)

    # ---------------- LVGI ----------------
    liab_names = ["Total Liab", "Total Liabilities Net Minority Interest"]
    liab_cy = safe_get(BS, liab_names, CY)
    liab_py = safe_get(BS, liab_names, PY)

    LVGI = (liab_cy / (ta + 1e-9)) / (liab_py / (ta_py + 1e-9) + 1e-9)

    # ---------------- TATA (FIXED PROPERLY) ----------------
    wc_cy = safe_get(BS, ["Total Current Assets"], CY) - safe_get(BS, ["Total Current Liabilities"], CY)
    wc_py = safe_get(BS, ["Total Current Assets"], PY) - safe_get(BS, ["Total Current Liabilities"], PY)

    if pd.isna(wc_cy) or pd.isna(wc_py):
        TATA = 0
    else:
        TATA = (wc_cy - wc_py) / (ta + 1e-9)

    # ---------------- FINAL M-SCORE ----------------
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
        "DSRI": DSRI,
        "GMI": GMI,
        "AQI": AQI,
        "SGI": SGI,
        "DEPI": DEPI,
        "SGAI": SGAI,
        "LVGI": LVGI,
        "TATA": TATA,
        "M_SCORE": M
    }

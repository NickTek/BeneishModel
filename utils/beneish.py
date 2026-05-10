from utils.parsers import safe_get


def calculate_beneish_score(BS, PL, CY, PY):

    # -----------------------
    # Revenue / Sales
    # -----------------------
    revenue_names = [
        "Total Revenue",
        "Operating Revenue",
        "Revenue",
    ]

    revenue_cy = safe_get(PL, revenue_names, CY)
    revenue_py = safe_get(PL, revenue_names, PY)

    # -----------------------
    # DSRI
    # -----------------------
    ar_names = [
        "Accounts Receivable",
        "Net Receivables",
    ]

    DSR_CY = safe_get(BS, ar_names, CY) / (revenue_cy + 1e-9)
    DSR_PY = safe_get(BS, ar_names, PY) / (revenue_py + 1e-9)

    DSRI = DSR_CY / (DSR_PY + 1e-9)

    # -----------------------
    # GMI
    # -----------------------
    cost_names = [
        "Cost Of Revenue",
        "Cost Of Goods Sold",
        "Cost of Revenue",
    ]

    cost_cy = safe_get(PL, cost_names, CY)
    cost_py = safe_get(PL, cost_names, PY)

    GM_CY = (revenue_cy - cost_cy) / (revenue_cy + 1e-9)
    GM_PY = (revenue_py - cost_py) / (revenue_py + 1e-9)

    GMI = GM_PY / (GM_CY + 1e-9)

    # -----------------------
    # AQI
    # -----------------------
    current_assets_names = [
        "Total Current Assets"
    ]

    assets_names = [
        "Total Assets"
    ]

    CA_CY = safe_get(BS, current_assets_names, CY)
    CA_PY = safe_get(BS, current_assets_names, PY)

    TA_CY = safe_get(BS, assets_names, CY)
    TA_PY = safe_get(BS, assets_names, PY)

    AQI = ((TA_CY - CA_CY) / (TA_CY + 1e-9)) / ((TA_PY - CA_PY) / (TA_PY + 1e-9))

    # -----------------------
    # SGI
    # -----------------------
    SGI = revenue_cy / (revenue_py + 1e-9)

    # -----------------------
    # DEPI
    # -----------------------
    dep_names = [
        "Depreciation",
        "Depreciation & Amortization",
        "Depreciation And Amortisation",
    ]

    dep_cy = safe_get(PL, dep_names, CY)
    dep_py = safe_get(PL, dep_names, PY)

    DEPI = (dep_py / (dep_py + TA_PY + 1e-9)) / (dep_cy / (dep_cy + TA_CY + 1e-9))

    # -----------------------
    # SGAI
    # -----------------------
    sga_names = [
        "Operating Expenses",
        "Other Expenses",
        "Selling General Administrative",
    ]

    sga_cy = safe_get(PL, sga_names, CY)
    sga_py = safe_get(PL, sga_names, PY)

    SGAI = (sga_cy / (revenue_cy + 1e-9)) / (sga_py / (revenue_py + 1e-9))

    # -----------------------
    # LVGI (FIXED ERROR)
    # -----------------------
    liab_names = [
        "Total Liab",
        "Total Liabilities Net Minority Interest",
        "Total Liabilities",
    ]

    LV_CY = safe_get(BS, liab_names, CY) / (TA_CY + 1e-9)
    LV_PY = safe_get(BS, liab_names, PY) / (TA_PY + 1e-9)

    LVGI = LV_CY / (LV_PY + 1e-9)

    # -----------------------
    # TATA
    # -----------------------
    curr_liab_names = [
        "Total Current Liabilities"
    ]

    WC_CY = safe_get(BS, current_assets_names, CY) - safe_get(BS, curr_liab_names, CY)
    WC_PY = safe_get(BS, current_assets_names, PY) - safe_get(BS, curr_liab_names, PY)

    TATA = (WC_CY - WC_PY) / (TA_CY + 1e-9)

    # -----------------------
    # M-SCORE
    # -----------------------
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

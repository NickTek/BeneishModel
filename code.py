
import pandas as pd
BS=pd.read_csv("filepath\filename.csv",index_col=0,header=0)
PL=pd.read_csv("filepath\filename.csv",index_col=0,header=0)

# print(BS.columns.values)
# print(BS.columns[1].values.dtypes)
print(BS.columns)
#
# a=input('Enter line item:')
# CY=input('Enter Current Year:')
# PY=input('Enter Previous Year:')
CY='Mar-20'
PY='Mar-19'
# print(BS.loc[a,b])

#Days’ Sales in Receivables Index (DSRI)
DSR_CY=BS.loc['Trade Receivables',CY]/PL.loc['Revenue From Operations [Net]',CY]
DSR_PY=BS.loc['Trade Receivables',PY]/PL.loc['Revenue From Operations [Net]',PY]
DSRI=DSR_CY/DSR_PY
print(DSRI)

#Gross Margin Index (GMI)
CostOfSales_CY=PL.loc['Cost Of Materials Consumed',CY]+PL.loc['Operating And Direct Expenses',CY]+PL.loc['Changes In Inventories Of FG,WIP And Stock-In Trade',CY]
CostOfSales_PY=PL.loc['Cost Of Materials Consumed',PY]+PL.loc['Operating And Direct Expenses',PY]+PL.loc['Changes In Inventories Of FG,WIP And Stock-In Trade',PY]
GM_CY=(PL.loc['Revenue From Operations [Net]',CY]-CostOfSales_CY)/PL.loc['Revenue From Operations [Net]',CY]
GM_PY=(PL.loc['Revenue From Operations [Net]',PY]-CostOfSales_PY)/PL.loc['Revenue From Operations [Net]',PY]
GMI=GM_PY/GM_CY
print(GMI)

#Asset Quality Index (AQI)
Assets_CY=1-((BS.loc['Total Current Assets',CY]+BS.loc['Fixed Assets',CY])/BS.loc['Total Assets',CY])
Assets_PY=1-((BS.loc['Total Current Assets',PY]+BS.loc['Fixed Assets',PY])/BS.loc['Total Assets',PY])
AQI=Assets_CY/Assets_PY
print(AQI)

# Sales Growth Index (SGI)
Sales_CY=PL.loc['Revenue From Operations [Net]',CY]
Sales_PY=PL.loc['Revenue From Operations [Net]',PY]
SGI=Sales_CY/Sales_PY
print(SGI)

# Depreciation Index (DEPI)
Dep_CY=(PL.loc['Depreciation And Amortisation Expenses',CY]/(PL.loc['Depreciation And Amortisation Expenses',CY]+BS.loc['Fixed Assets',CY]))
Dep_PY=(PL.loc['Depreciation And Amortisation Expenses',PY]/(PL.loc['Depreciation And Amortisation Expenses',PY]+BS.loc['Fixed Assets',PY]))
DEPI=Dep_PY/Dep_CY
print(DEPI)

#Sales, General, and Administrative expenses Index (SGAI)
SGA_CY=PL.loc['Other Expenses',CY]/PL.loc['Revenue From Operations [Net]',CY]
SGA_PY=PL.loc['Other Expenses',PY]/PL.loc['Revenue From Operations [Net]',PY]
SGAI=SGA_CY/SGA_PY
print(SGAI)

# Leverage Index (LVGI)
LV_CY=(BS.loc['Total Non-Current Liabilities',CY]+BS.loc['Total Current Liabilities',CY])/BS.loc['Total Assets',CY]
LV_PY=(BS.loc['Total Non-Current Liabilities',PY]+BS.loc['Total Current Liabilities',PY])/BS.loc['Total Assets',PY]
LVGI=LV_CY/LV_PY
print(LVGI)

#Total Accruals to Total Assets
Change_WC=(BS.loc['Total Current Assets',CY]-BS.loc['Total Current Liabilities',CY])-(BS.loc['Total Current Assets',PY]-BS.loc['Total Current Liabilities',PY])
Change_Cash=(BS.loc['Cash And Cash Equivalents',CY]-BS.loc['Cash And Cash Equivalents',PY])
TATA=(Change_WC-Change_Cash-PL.loc['Depreciation And Amortisation Expenses',CY])/BS.loc['Total Assets',CY]
print(TATA)

##M-Score
M=-4.84 + 0.92* DSRI +0.528*GMI + 0.404*AQI+ 0.892*SGI + 0.115*DEPI-0.172*4.679*TATA-0.327*LVGI
print('The M-socre/Beneish M Score is:  '+str(M))
print('A M-score > -2.22 implies that the financial statements MAY have been manipulated')




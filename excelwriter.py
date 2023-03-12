import pandas as pd

def writeToExcel(excel_sheets, filename):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    filepath='C:/Users/sc176/OneDrive/Desktop/Excel Automation/AutomationTestScript/Result/'+filename+'.xlsx'
    
    with pd.ExcelWriter('C:/Users/sc176/OneDrive/Desktop/Excel Automation/AutomationTestScript/Result/'+filename+'.xlsx', engine='xlsxwriter') as writer:
        #write dataframe to excel
        for s in excel_sheets.keys():
            excel_sheets[s].to_excel(writer,sheet_name=s,encoding='utf-8')#check once whether we need utf-8
        


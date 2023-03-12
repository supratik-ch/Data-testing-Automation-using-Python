import getdata
import datetime as dt
import datacompare
import pandas as pd
import excelwriter

filenames=['excelfile1','excelfile2']
primary_cols={'excelfile1':'EMPLOYEE_ID','excelfile2':'EMPLOYEE_ID'}

excel_file1 = getdata.readExcelData("C:\\Users\\sc176\\OneDrive\\Desktop\\Excel Automation\\AutomationTestScript\\resource\\"+filenames[0]+".xlsx")
excel_file2 = getdata.readExcelData("C:\\Users\\sc176\\OneDrive\\Desktop\\Excel Automation\\AutomationTestScript\\resource\\"+filenames[1]+".xlsx")

def excelcompare(excel1, excel2):
    output_file_name=str(filenames[0]+'_'+filenames[1]+'_'+dt.datetime.now().strftime("%Y_%m_%d-%H%M%S"))
    df_left=datacompare.getDifferencesforExcel(excel_file1,excel_file2,primary_cols['excelfile1'],primary_cols['excelfile2'],"left_only")
    df_right=datacompare.getDifferencesforExcel(excel_file1,excel_file2,primary_cols['excelfile1'],primary_cols['excelfile2'],"right_only")
    df_both=datacompare.getDifferencesforExcel(excel_file1,excel_file2,primary_cols['excelfile1'],primary_cols['excelfile2'],"both")

    excel1_df_data=df_both.copy()
    excel2_df_data=df_both.copy()
    drop_x(excel1_df_data)
    drop_y(excel2_df_data)
    strip_right(excel1_df_data,'_y')
    strip_right(excel2_df_data,'_x')

    df_total,df_mismatches,mat_cnt,mis_cnt=datacompare.compareForExcel(excel1_df_data,excel2_df_data,primary_cols['excelfile1'],primary_cols['excelfile2'])
    
    df_final=pd.DataFrame({'Record Count in Src Table':excel_file1.shape[0],
                               'Record Count in Tgt Table':excel_file2.shape[0],
                               'Records missing in Src Table':df_right.shape[0],
                               'Records missing in Tgt Table':df_left.shape[0],
                               'Total Records Matched':df_both.shape[0],
                               'Total Records Mismatched':df_mismatches.shape[0],
                               'Total Cells Matched':mat_cnt,
                               'Total Cells Mismatched':mis_cnt
                               },
                               index=[0])
        
    excel_sheets={'Summary':df_final,'Src table data':excel_file1,'Tgt table data':excel_file2,'Records missing in Src':df_right,'Records missing in Tgt':df_left,'Matched Rows':df_both,'Mismatch Rows':df_mismatches,'Complete Result Set':df_total}
    excelwriter.writeToExcel(excel_sheets,output_file_name)


def drop_y(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y') or x.endswith('_merge')]
    df.drop(to_drop, axis=1, inplace=True)

def drop_x(df):
    # list comprehension of the cols that end with '_x'
    to_drop = [x for x in df if x.endswith('_x') or x.endswith('_merge')]
    df.drop(to_drop, axis=1, inplace=True)

def strip_right(df, suffix):
    df.columns = df.columns.str.rstrip(suffix)
import datetime as dt
import dbconn
import getdata
import datacompare
import pandas as pd
import excelwriter

src_query=''
tgt_query=''
tbNames=''
primaryCols=''

data1=[]
excel_file = getdata.readExcelData("C:\\Users\\sc176\\OneDrive\\Desktop\\Excel Automation\\AutomationTestScript\\resource\\data.xlsx")

def readSrcQuery(excel_file):
    print('Reading Src Query')
    values=[]
    for i in range(len(excel_file)):
        if (excel_file['Run Marker'][i]) == 'Y':
            values.append(excel_file['Source Query'][i])
    return values

def readTgtQuery(excel_file):
    print('Reading Tgt Query')
    values=[]
    for i in range(len(excel_file)):
        if (excel_file['Run Marker'][i]) == 'Y':
            values.append(excel_file['Target Query'][i])
    return values

def readTableName(excel_file):
    print('Reading Table Name')
    values=[]
    for i in range(len(excel_file)):
        if (excel_file['Run Marker'][i]) == 'Y':
            values.append(excel_file['Tablename'][i])
    return values

def readTablePrimaryColumns(excel_file):
    print('Reading Table Primary Columns')
    values=[]
    for i in range(len(excel_file)):
        if (excel_file['Run Marker'][i]) == 'Y':
            values.append(excel_file['Primary Column'][i])
    return values

def readDataFromExcel(excel_file):
    global src_query
    global tgt_query
    global tbNames
    global primaryCols
    src_query=readSrcQuery(excel_file)
    tgt_query=readTgtQuery(excel_file)
    tbNames=readTableName(excel_file)
    primaryCols=readTablePrimaryColumns(excel_file)

def dbcompare(excel_file):
    readDataFromExcel(excel_file)
    for i in range(len(tbNames)):
        output_file_name=str(tbNames[i]+'_'+dt.datetime.now().strftime("%Y_%m_%d-%H%M%S"))
        conn=dbconn.getDbConnection()
        print('Connection String --->  ',conn)
        src_data=dbconn.getData(src_query[i],conn)
        tgt_data=dbconn.getData(tgt_query[i],conn)
        df_left=datacompare.getDifferences(i,src_data,tgt_data,primaryCols,"left_only")
        df_right=datacompare.getDifferences(i,src_data,tgt_data,primaryCols,"right_only")
        df_both=datacompare.getDifferences(i,src_data,tgt_data,primaryCols,"both")

        src_df_data=df_both.copy()
        tgt_df_data=df_both.copy()
        drop_x(src_df_data)
        drop_y(tgt_df_data)
        strip_right(tgt_df_data,'_x')
        strip_right(src_df_data,'_y')
        
        df_total,df_mismatches,mat_cnt,mis_cnt=datacompare.compare(i,src_df_data,tgt_df_data,primaryCols)

        df_final=pd.DataFrame({'Record Count in Src Table':src_data.shape[0],
                               'Record Count in Tgt Table':tgt_data.shape[0],
                               'Records missing in Src Table':df_right.shape[0],
                               'Records missing in Tgt Table':df_left.shape[0],
                               'Total Records Matched':df_both.shape[0],
                               'Total Records Mismatched':df_mismatches.shape[0],
                               'Total Cells Matched':mat_cnt,
                               'Total Cells Mismatched':mis_cnt
                               },
                               index=[0])
        
        excel_sheets={'Summary':df_final,'Src table data':src_data,'Tgt table data':tgt_data,'Records missing in Src':df_right,'Records missing in Tgt':df_left,'Matched Rows':df_both,'Mismatch Rows':df_mismatches,'Complete Result Set':df_total}
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

import pandas as pd
import os

def readExcelData(path):
    df_excel=[]
    df_read=pd.ExcelFile(path)  
    for sheet in df_read.sheet_names:
        df=pd.read_excel(path,sheet_name=sheet)
        df_excel.append(df)
    return df_read.sheet_names,df_excel

def getSheetNames(path):
    df_read=pd.ExcelFile(path) 
    return df_read.sheet_names

def find_files(filename, search_path):
    r=''
    for root,dir,files in os.walk(search_path):
        if filename in files:
            r=(os.path.join(root,filename))
    return r

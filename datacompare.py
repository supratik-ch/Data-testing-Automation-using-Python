import numpy as np

def getDifferences(i,dataframe1,dataframe2,primary_key,ind=None):
    pkeys=primary_key[i].split(',')
    df_compare=dataframe1.merge(dataframe2,indicator=True,how="outer",left_on=pkeys,right_on=pkeys)

    if ind is None:
        diff_df=df_compare[df_compare["_merge"] != "both"]
    else:
        diff_df=df_compare[df_compare["_merge"] == ind]

    return diff_df

def compare(i,dataframe1,dataframe2,primary_key,strip_spaces=True,fill_na=True):
    mis_cnt=0
    mat_cnt=0
    pkeys=primary_key[i].split(",")

    df1= dataframe1.sort_values(by=pkeys) 
    df2= dataframe2.sort_values(by=pkeys)

    for col in df1.select_dtypes(include=['object']).columns:
        df1[col]=df1[col].str.strip()
    for col in df2.select_dtypes(include=['object']).columns:
        df2[col]=df2[col].str.strip()

    df1 = df1.fillna("")
    df2 = df2.fillna("")

    comparison_values = df1.values == df2.values

    compared_df1=df1.compare(df2,keep_shape=True,keep_equal=True)
    compared_df2=df1.compare(df2)

    rows1,cols1=np.where(comparison_values==True)
    for item in list(zip(rows1,cols1)):
       df1.iloc[item[0], item[1]] = 'MATCHED'
       mat_cnt+=1
    rows2,cols2=np.where(comparison_values==False)
    for item in zip(rows2,cols2):
       df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])
       mis_cnt+=1  

    return compared_df1,compared_df2,mat_cnt,mis_cnt

import cx_Oracle as orcl
import pandas as pd

def getDbConnection():    
    try:
        conn=orcl.connect('sys/orcl@localhost:1521/orclpdb',mode=orcl.SYSDBA)
        return conn
    except orcl.DatabaseError as er:
        print('There is an error in the Oracle database:', er)

def getData(query,connection):
    data=pd.read_sql(query,connection)
    return data
    
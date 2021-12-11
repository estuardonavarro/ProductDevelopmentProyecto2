# ---- Import libraries ----
import pandas as pd
import mysql.connector


def connect_to_database(query):
    """
    Connect to a database.
    """
    server = 'db' 
    database = 'test'
    port = '3306'
    username = 'test' 
    passwd = 'test123'
    #driver='{ODBC Driver 17 for SQL Server}'
    
    # Connect to the database
    cnx = mysql.connector.connect(user=username, password=passwd,
                              host=server,
                              database=database, port=port)
    #cnx.close()
    # Consulta a la base de datos
    frase = query
    df= pd.read_sql_query(frase, cnx)
    return df

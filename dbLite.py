import sqlite3
import os
import pandas as pd

class DbLite:

    def __init__(self, db):
        self.db=db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
 
    def readPandasFromDB(self, table):
        table = pd.read_sql_query("select * from "+table+";", self.conn)
        return table

    def writePandasToDB(self, table, dataFrame, create=False):
        
        if create == True:
            dataFrame.to_sql(table, con=self.conn, if_exists='replace', index=False)
        else:
            sameDateRows = pd.read_sql_query("select * from "+table+" WHERE date='"+dataFrame['date'][0].strftime('%Y-%m-%d')+"';", con=self.conn)

            if sameDateRows.empty:
                print("Writing new rows to database")
                dataFrame.to_sql(table, con=self.conn, if_exists='append', index=False)
            else:
                print("Rows already exist in database")
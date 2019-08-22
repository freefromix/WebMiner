import pandas as pd
import yfinance as yf
import sqlite3
import os

import requests as _requests
import numpy as np

class CompanyYf:

    def __init__(self, ticker):
        self.ticker = ticker

    def readFromDatabase(self):
        table = self.ticker.replace(".", "_")
        conn = sqlite3.connect("db"+os.sep+"balanceSheet.db")
        table = pd.read_sql_query("select * from "+table+";", conn)
        return table

    def writeToDatabase(self):
        table = self.ticker.replace(".", "_")
        conn = sqlite3.connect("db"+os.sep+"balanceSheet.db")
        self.balance_sheet.to_sql(table, con=conn, if_exists='replace', index_label='id')

    def get_yf_data(self):
        companyData = yf.Ticker(self.ticker)
        self.balance_sheet = companyData.get_balance_sheet()
        
#        self.cashflow = companyData.get_cashflow()
#        self.income_statement = companyData.get_financials()
#        self.dividends = companyData.get_dividends()
#        self.actions = companyData.get_actions()
#        self.splits = companyData.get_splits()
#        self.history = companyData.history()
#        self.info = companyData.info

    def get_fundamentals(self, kind, proxy=None):
        # setup proxy in requests format
        if proxy is not None:
            if isinstance(proxy, dict) and "https" in proxy:
                proxy = proxy["https"]
            proxy = {"https": proxy}
        url = '%s/%s/%s' % ('https://finance.yahoo.com/quote', self.ticker, kind)
        data = pd.read_html(_requests.get(url=url, proxies=proxy).text)[0]
        print(_requests.get(url=url, proxies=proxy).text)
        data.columns = [''] + list(data[:1].values[0][1:])
        data.set_index('', inplace=True)
        for col in data.columns:
            data[col] = np.where(data[col] == '-', np.nan, data[col])
        idx = data[data[data.columns[0]] == data[data.columns[1]]].index
        data.loc[idx] = '-'
        return data[1:]

testit = CompanyYf("CVV.V")
testit.get_fundamentals('balance-sheet')

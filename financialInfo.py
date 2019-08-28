from yahoofinancials import YahooFinancials
import os
from tinydb import TinyDB, Query
import json


class CompanyFinance:

    def __init__(self, ticker):
        self.ticker = ticker

    def writeToTinyDb(self, tableName, newData):
        db=TinyDB('db/'+self.ticker+'.json')
        table=db.table(tableName)

        for dataRecord in newData:
            dataDate=list(dataRecord.keys())[0]
            result=table.search(Query()[dataDate])

            if result == []:
                print(dataDate + ' record does not exist into database. Writing it!')
                table.insert(dataRecord)
            else:
                print(dataDate + ' exist into database')

    def readFromTinyDb(self):
        db=TinyDB('db/'+self.ticker+'.json')
        return db.all()

    def get_balanceSheet(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('annual', 'balance')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

    def get_balanceSheetQ(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('quarterly', 'balance')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

    def get_incomeStatement(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('annual', 'income')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

    def get_incomeStatementQ(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('quarterly', 'income')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

    def get_cashFlow(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('annual', 'cash')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

    def get_cashFlowQ(self):
        companyData=YahooFinancials(self.ticker)
        stmts=companyData.get_financial_stmts('quarterly', 'cash')
        stmtsValues=stmts[list(stmts.keys())[0]][self.ticker]
        tableName=list(stmts.keys())[0]
        return (stmtsValues[::-1], tableName)

#    def get_dividends(self):
#        companyData=yf.Ticker(self.ticker)
#        self.dividends=companyData.get_dividends()
#        return self.dividends
#
#    def get_actions(self):
#        companyData=yf.Ticker(self.ticker)
#        self.actions=companyData.get_actions()
#        return self.actions
#
#    def get_splits(self):
#        companyData=yf.Ticker(self.ticker)
#        self.splits=companyData.get_splits()
#        return self.splits
#
#    def get_history(self):
#        companyData=yf.Ticker(self.ticker)
#        self.history=companyData.history()
#        return self.history
#
#    def get_info(self):
#        companyData=yf.Ticker(self.ticker)
#        self.info=companyData.info
#        return self.info
#
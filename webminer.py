from dailysentiment import DailySentiment
import sqlite3
import os
import json
from financialInfo import CompanyFinance


def daylySentiment():
    dailys = DailySentiment("db"+os.sep+"dailySentiment.db")
    dailys.writePandasToDB('dailySentiment', dailys.getDailySentiment())
    fullTable = dailys.readPandasFromDB('dailySentiment')
    print(fullTable)
    dailys.getDatesFromBegining('dailySentiment', dailys.getStartDate())


def financialInfos():
    company = CompanyFinance("CVV.V")

    balanceSheet, tableName = company.get_balanceSheet()
    company.writeToTinyDb(tableName, balanceSheet)
    incomeStatement, tableName = company.get_incomeStatement()
    company.writeToTinyDb(tableName, incomeStatement)
    cashFlow, tableName = company.get_cashFlow()
    company.writeToTinyDb(tableName, cashFlow)

    balanceSheetQ, tableName = company.get_balanceSheetQ()
    company.writeToTinyDb(tableName, balanceSheetQ)
    incomeStatementQ, tableName = company.get_incomeStatementQ()
    company.writeToTinyDb(tableName, incomeStatementQ)
    cashFlowQ, tableName = company.get_cashFlowQ()
    company.writeToTinyDb(tableName, cashFlowQ)

def testIt():
    from yahoofinancials import YahooFinancials

    companyData = YahooFinancials("CVV.V")
    result = companyData.get_stock_price_data()
    print(result)

#financialInfos()
testIt()
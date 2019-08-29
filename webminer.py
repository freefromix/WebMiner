from dailysentiment import DailySentiment
from financialInfo import CompanyFinance
import os
import json


def getFinancialInfos():
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

def getDailySentiment():
    tableName = "dailySentiment"
    dailys = DailySentiment(tableName)
    dailysentiment = dailys.getDailySentiment()
    dailys.writeToTinyDb(tableName, dailysentiment)

getDailySentiment()
getFinancialInfos()

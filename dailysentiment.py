import sqlite3
import requests
import pandas as pd
from datetime import date
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import timedelta

class DailySentiment:

    def __init__(self, db):
        self.startDate = date(2019, 8, 20)
        self.db=db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        page = requests.get("http://www.tag618.com/services")
        soup = BeautifulSoup(page.content, 'html.parser')
        self.dailyDate = self._scrapDailyDate(soup)
        dailySentimentTmp = self._scrapTableDailySentiment(soup)
        sLength = len(dailySentimentTmp[dailySentimentTmp.columns[0]])
        columnToAdd = [self.dailyDate] * sLength
        dailySentimentTmp['date'] = pd.Series(columnToAdd)
        self.dailySentiment = dailySentimentTmp

    def _scrapDailyDate(self, soup):
        dateSpanTag = soup.find('span', attrs={'style': 'font-size: 14px;'})
        text = dateSpanTag.find('b').text
        numbers = re.findall(r'\d+', text)
        dayOfDsi = date.today().replace(day=int(numbers[0]))
        return dayOfDsi

    def _scrapTableDailySentiment(self, soup):
        table = soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        dfStr = self._convertListToDataFrame(data)
        dfNumeric = self._convertDfStrToNumeric(dfStr)
        return dfNumeric

    def _convertListToDataFrame(self, toConvert):
        labels = toConvert[0]
        data = toConvert[1:]
        df = pd.DataFrame.from_records(data, columns=labels)
        return df

    def _convertDfStrToNumeric(self, toConvert):
        cols = toConvert.columns.drop('INSTRUMENT')
        toConvert[cols] = toConvert[cols].apply(pd.to_numeric, errors='coerce')
        return toConvert

    def readPandasFromDB(self, table):
        table = pd.read_sql_query("select * from "+table+";", self.conn)
        return table

    def writePandasToDB(self, table, dataFrame, create=False):
        if create == True:
            dataFrame.to_sql(table, con=self.conn,
                             if_exists='replace', index=False)
        else:
            sameDateRows = pd.read_sql_query(
                "select * from "+table+" WHERE date='"+dataFrame['date'][0].strftime('%Y-%m-%d')+"';", con=self.conn)

            if sameDateRows.empty:
                print("Writing new rows to database")
                dataFrame.to_sql(table, con=self.conn,
                                 if_exists='append', index=False)
            else:
                print("Rows already exist in database")

    def getDatesFromBegining(self, table, startDate):
        dt = datetime.combine(startDate, datetime.min.time())
        for i in range(100):
            dt += timedelta(days=1)
            print(dt.date())

    def getDailySentiment(self):
        return self.dailySentiment

    def getDailyDate(self):
        return self.dailyDate

    def getStartDate(self):
        return self.startDate

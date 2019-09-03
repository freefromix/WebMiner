from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd
import requests
import re
import os
import json

class DailySentiment:

    def __init__(self, filename):
        self.startDate = date(2019, 8, 20)
        self.filename = "db/"+filename+".json"

    def _scrapDailyDate(self, soup):
        dateSpanTag = soup.find('span', attrs={'style': 'font-size: 14px;'})
        text = dateSpanTag.find('b').text
        numbers = re.findall(r'\d+', text)

        dayOfDsi = int(numbers[0])
        dayToday = int(date.today().day)
        dateOfDsi = date.today().replace(day=int(numbers[0]))

        if dayToday >= dayOfDsi:
            dateOfDsi = date.today().replace(day=dayOfDsi)
        else:
            dateOfDsi = date.today().replace(month=int(date.today().month)-1, day=dayOfDsi)

        return dateOfDsi

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

    def writeToTinyDb(self, tableName, newData):
        db = TinyDB(self.filename)
        table = db.table(tableName)

        dataDate = newData['date']
        result = table.search(Query().date == dataDate)

        if result == []:
            print(dataDate + ' record does not exist into database. Writing it!')
            table.insert(newData)
        else:
            print(dataDate + ' exist into database')

    def readFromTinyDb(self, tableName):
        db = TinyDB(self.filename)
        table = db.table(tableName)
        return table.all()

    def getDailySentiment(self):
        page = requests.get("http://www.tag618.com/services")
        soup = BeautifulSoup(page.content, 'html.parser')

        self.dailyDate = self._scrapDailyDate(soup)

        dailySentimentPds = self._scrapTableDailySentiment(soup)

        dailySentimentDictByInstrument = self._transformPandasToDict(
            dailySentimentPds)

        self.dailySentiment = self._addDateToDict(dailySentimentDictByInstrument)

        return self.dailySentiment

    def _transformPandasToDict(self, dailySentimentPds):
        dailySentimentDict = dailySentimentPds.to_dict(orient='records')

        dailySentimentDictByInstrument = {}
        for record in dailySentimentDict:
            instrument = record.pop('INSTRUMENT')
            dailySentimentDictByInstrument[instrument] = record

        return dailySentimentDictByInstrument

    def _addDateToDict(self, dailySentimentDictByInstrument):
        datedDailySentiment = {}
        datedDailySentiment['date'] = self.dailyDate.isoformat() 

        datedDailySentiment.update(dailySentimentDictByInstrument)
        return datedDailySentiment

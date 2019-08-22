import requests
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
import re
import os
from dbLite import DbLite
from bs4 import BeautifulSoup


class DailySentiment:

    def __init__(self):
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

    def getDailySentiment(self):
        return self.dailySentiment

    def getDailyDate(self):
        return self.dailyDate

    def getDatesFromBegining(self):
        mydate = date(2003,2,28)
        dt = datetime.combine(mydate, datetime.min.time())
        print(type(dt))
        for i in range(5):
            dt += timedelta(days=1)
    

dailys = DailySentiment()
db = DbLite("db"+os.sep+"dailySentiment.db")
db.writePandasToDB('dailySentiment', dailys.getDailySentiment())
fullTable = db.readPandasFromDB('dailySentiment')
print(fullTable)



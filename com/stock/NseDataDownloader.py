'''
Created on 09-May-2017

@author: fly
'''

from nsepy import get_history
from ConfigReader import processCSVFile
from datetime import date,  timedelta


def downloadNseData(rows) :
    print("Start Fetching data from NSE...")
    for row in rows :
        try:
            exchangeId,stockName,timeDelay,days,companyName = row[0:5]
            if (exchangeId == 'NSE') :            
                endDate = date.today() - timedelta(days=1) 
                startDate =  endDate - timedelta(days=int(days)) 
                dataframe = get_history(symbol=stockName,start=startDate,end=endDate)
                dataframe.drop('Symbol', axis=1, inplace=True)
                dataframe.drop('Series', axis=1, inplace=True)
                dataframe.to_csv('dataset/{0}.csv'.format(exchangeId+'_'+companyName),sep=',', encoding='utf-8')
        except :
            print ("Error while downloding data")
            
# main executor              
if __name__ == '__main__':    
    rows =processCSVFile('config/inputConfig.csv')
    downloadNseData(rows)
    print("Process Completed...")
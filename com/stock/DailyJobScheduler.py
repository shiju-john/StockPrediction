'''
Created on 08-May-2017

@author: fly
'''



from datetime import datetime
from threading import Timer
import ConfigReader
import GFinanceDataDownloader



def schedule_Job(job):
    x=datetime.today()
    y = x.replace(day=x.day, hour=15, minute=35, second=x.second, microsecond=0)
    if(x < y) :
        y = x.replace(day=x.day, hour=15, minute=35, second=x.second, microsecond=0)
    else :
        y=x.replace(day=x.day+1, hour=15, minute=35, second=x.second, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1
    t = Timer(secs, job)
    t.start()

    
def addDailyData():
    print("Job Started ")
    rows = ConfigReader.processCSVFile('config/inputConfig.csv')
    for row in rows:
        exchangeId,stockName,timeDelay,days,companyName = row[0:5] 
        q = GFinanceDataDownloader.GoogleFinanceQuote(exchangeId,stockName,0,0)              
        q.write_csv('dataset/{0}.csv'.format(exchangeId+'_'+companyName),'a') 
    #schedule_Job(addDailyData)

#schedule_Job(addDailyData)
addDailyData()
        
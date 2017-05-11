'''
Created on 08-May-2017

@author: fly
'''

import urllib,datetime
from  ConfigReader import processCSVFile

class Quote(object):
  
    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'
  
    def __init__(self):
        self.symbol = ''
        self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))

    def append(self,dt,open_,high,low,close,volume):
        self.date.append(dt.date())
        self.time.append(dt.time())
        self.open_.append(float(open_))
        self.high.append(float(high))
        self.low.append(float(low))
        self.close.append(float(close))
        self.volume.append(int(volume))
      
    def to_csv(self):
        return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
                  self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
                  self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar]) 
                  for bar in xrange(len(self.close))])
        
    def write_csv(self,filename,mode):
        headers = 'symbol,date,Time,open,high,low,close,volume\n'
        with open(filename,mode) as f:
            if(mode=='a'):
                data =  self.to_csv()
            else : 
                data =  headers + self.to_csv()
            f.write (data) 
            
    def read_csv(self,filename):
        self.symbol = ''
        self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        for line in open(filename,'r'):
            symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
            self.symbol = symbol
            dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
            self.append(dt,open_,high,low,close,volume)
        return True

    def __repr__(self):
        return self.to_csv()




class GoogleFinanceQuote(Quote):
 
    def __init__(self,exchangeName,symbol,interval_seconds=300,num_days=5):
        super(GoogleFinanceQuote,self).__init__()
        self.symbol = symbol.upper()
        url_string = "http://www.google.com/finance/getprices?q={0}".format(self.symbol)
        url_string += "&x={0}&i={1}&p={2}d&f=d,o,h,l,c,v".format(exchangeName,interval_seconds,num_days)
        csv = urllib.urlopen(url_string).readlines()        
      
        for bar in xrange(7,len(csv)):
            if csv[bar].count(',')!=5: continue
            offset,close,high,low,open_,volume = csv[bar].split(',')
            if offset[0]=='a':
                day = float(offset[1:])
                offset = 0
            else:
                offset = float(offset)
            open_,high,low,close = [float(x) for x in [open_,high,low,close]]
            dt = datetime.datetime.fromtimestamp(day+(interval_seconds*offset))
            self.append(dt,open_,high,low,close,volume)
   
    
# Download the configured stock data  
def downloadData(rows):  
    for row in rows:
        exchangeId,stockName,timeDelay,days,companyName = row[0:5] 
        q = GoogleFinanceQuote(exchangeId,stockName,float(timeDelay),float(days))              
        q.write_csv('dataset/{0}.csv'.format(exchangeId+'_'+companyName),'w')

# main executor              
if __name__ == '__main__':
    rows =processCSVFile('config/inputConfig.csv') 
    downloadData(rows)   
    
    
    
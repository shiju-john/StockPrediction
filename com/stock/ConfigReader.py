'''
Created on 08-May-2017

@author: fly
'''

import csv
import GFinanceDataDownloader 


# Read the configuration file and return the configuration data as list data 
def processCSVFile(fileName):    
    rows = []
    with open(fileName, "rb") as f_obj:        
        next(f_obj, None) # SKIP header 
        reader = csv.reader(f_obj)
        for row in reader:
            if(len (row)<5):
                raise ValueError('Wrong Input Configuration')
            else :
                rows.append(row)
               
    return  rows 


# Download the configured stock data  
def downloadData(rows):  
    for row in rows:
        exchangeId,stockName,timeDelay,days,companyName = row[0:5] 
        q = GFinanceDataDownloader.GoogleFinanceQuote(exchangeId,stockName,float(timeDelay),float(days))              
        q.write_csv('dataset/{0}.csv'.format(exchangeId+'_'+companyName),'w')




# main executor              
if __name__ == '__main__':
    rows =processCSVFile('config/inputConfig.csv') 
    downloadData(rows)
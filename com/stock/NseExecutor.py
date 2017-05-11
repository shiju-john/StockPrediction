'''
Created on 10-May-2017

@author: fly
'''
from InputConfig import readConfigurations
from TalibProcessor import processData
from NseDataDownloader import downloadNseData


if __name__ == '__main__':
    
    print ("Reading Configurations...")
    rows = readConfigurations('config/inputConfig.csv')
    
    print ("Downloading NSE data")
    downloadNseData(rows)
    
    print ("TALIB process started ")
    processData(rows)
    
    print ("Process Completed ...")
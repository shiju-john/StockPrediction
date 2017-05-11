'''
Created on 10-May-2017

@author: fly
'''
import ConfigReader
import TalibProcessor
import NseDataDownloader


if __name__ == '__main__':
    
    print ("Reading Configurations...")
    rows =ConfigReader.processCSVFile('config/inputConfig.csv')
    
    print ("Downloading NSE data")
    NseDataDownloader.downloadNseData(rows)
    
    print ("TALIB process started ")
    TalibProcessor.processData(rows)
    
    print ("Process Completed ...")
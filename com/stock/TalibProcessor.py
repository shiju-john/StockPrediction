'''
Created on 09-May-2017

@author: fly
'''
import ConfigReader
import numpy
import TalibConfigReader
from  dateutil.parser import parse
import os.path
from talib import abstract
import talib
import pandas
import time
import StockInput
import csv

def enrichTalibValues(inputDict, features, result) :
    headers=''
    for aType in features:
        for func in talib.get_function_groups()[aType]:
            pf = abstract.Function(func)
            try:
                pf.input_arrays = inputDict
                pf.run()
                outputs = pf.outputs
                if isinstance(outputs, list):
                    for anItem , name in zip(outputs, pf.output_names):
                        result = numpy.hstack((result, anItem.reshape(anItem.size,1)))
                        headers = ','.join([headers, name])
                else:
                    result = numpy.hstack((result, outputs.reshape(outputs.size,1)))
                    headers = ','.join([headers,func])
            except:
                print 
    return result, headers

def stripData(df,config):
    
    if config.hasRemoveNaNColumns() :
        df = df.dropna(axis=1,how="all")
    
    if config.hasRemoveNaNRows() :
        df = df.dropna(axis=0)
        
    if config.hasRemove_SameVal_Columns() :
        df = df.drop(df.std()[(df.std() == 0)].index, axis=1)
        
    return df  
    

def writeNormalizeFile(outFileName): 
    
    headerText=''
    with open('dataset/talib/{0}.csv'.format(outFileName)) as csvfile:
        rows=iter(csv.reader(csvfile)).next()
        headerText  =  str(rows)[1:-1]
    dataSet = numpy.genfromtxt('dataset/talib/{0}.csv'.format(outFileName), delimiter="," ,skip_header=True)
   
    stockInput = StockInput.StockInput(None)
    dataSet = stockInput.transform(dataSet)
    numpy.savetxt('dataset/talib/Normalize/{0}.csv'.format(outFileName), dataSet, delimiter=',', header =headerText)      
 


def parseDate(df):
    dates_list = [parse(dateValue) for dateValue in df['Date']]   
    datesvale = [time.mktime(dateValue.timetuple()) for dateValue in dates_list]
    df['Date'] = datesvale
    return df;    
     



def writeResult(inFilePath,outFileName ,headers,data,config):
    df = pandas.read_csv(inFilePath)
    count =0 
    for key in headers.split(',') :
        if key != '' :
            new_column = pandas.DataFrame({key: data[count]})
            df = df.merge(new_column, left_index = True, right_index = True)
        count = count +1
    #df = df.fillna('nan')  
    df =stripData(df,config)    
    df = parseDate(df)    
    df = df.to_csv('dataset/talib/{0}.csv'.format(outFileName),index=False, sep=',', encoding='utf-8')
    writeNormalizeFile(outFileName)


def processFile(fileName,config ): 
    
    dataFilePath = 'dataset/{0}.csv'.format(fileName) 
    
    if os.path.isfile(dataFilePath) :
           
        sample_data = numpy.genfromtxt(dataFilePath, delimiter=",", skip_header=True)
        sample_data = numpy.column_stack(sample_data)
        openValue = sample_data[config.getOpenIndex()].astype(float)
        high = sample_data[config.getHighIndex()].astype(float)
        low = sample_data[config.getLowIndex()].astype(float)
        close = sample_data[config.getCloseIndex()].astype(float)
        volume = sample_data[config.getVolumeIndex()].astype(float)
        result = numpy.empty(shape=(openValue.shape[0],1),dtype=float)
        
        inputDict = {'high':high,'close':close,'open':openValue,
                     'low':low,'volume':volume,'timeperiod':3}
        
        result, headers = enrichTalibValues(inputDict, config.getFeatures(), result)     
        result = numpy.column_stack(result)
        
        writeResult(dataFilePath,fileName,headers,result,config)
                
    else :
        #raise ValueError('File Not Found {0}'.format(fileName))
        print ('File Not Found {0}'.format(fileName))



def processData(rows):
    talibConfig = TalibConfigReader.TalibConfigReader('config/TalibConfig.ini')
    for row in rows:
        exchangeId,stockName,timeDelay,days,companyName = row[0:5]
        processFile(exchangeId+'_'+companyName,talibConfig)

# main executor              
if __name__ == '__main__':    
    rows = ConfigReader.processCSVFile('config/inputConfig.csv')
    processData(rows)
    
    
    
    
    
    
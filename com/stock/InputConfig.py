'''
Created on 08-May-2017

@author: fly
'''

import csv
import configparser

# Read the configuration file and return the configuration data as list data 
def readConfigurations(fileName):    
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


def readConfigFile(fileName):
    config = configparser.ConfigParser()
    config.sections()
    config.read(fileName)
    return config


class TalibConfigReader(object):
    '''
    Load the TA LIB configurations from the config/TalibConfig.ini
    
    Configuration contains TA library Features and column Index Of input values, These inputs are used
    for the invocation of TA Library functions.
         
    Column Index : Expected the index of the columns OPEN,HIGH,LOW,CLOSE,VOLUME in same order
    Features : List of features required for Input training 
    '''


    def __init__(self, fileName):
        '''
        Constructor
        '''
        config = readConfigFile(fileName)
        self.features = config['TA LIB CONFIG']['features'].split(',')
        #self.openColumnIndex = [int(x) for x in config['TA LIB CONFIG']['columnIndex'].split(',')]
        self.openIndex = int( config['TA LIB CONFIG']['open'])
        self.closeIndex = int( config['TA LIB CONFIG']['close'])
        self.highIndex = int( config['TA LIB CONFIG']['high'])
        self.lowIndex = int( config['TA LIB CONFIG']['low'])
        self.volumeIndex = int( config['TA LIB CONFIG']['volume'])
        
        
        # Filter arguments
        self.rFilter_remove_nan = bool(config['DATA_FILTER']['REMOVE_ANY_NaN_ROWS'])
        self.cFilter_remove_nan = bool(config['DATA_FILTER']['REMOVE_ALL_NaN_COLUMNS'])
        self.cFilter_remove_same_val = bool(config['DATA_FILTER']['REMOVE_SAME_VALUE'])
        
    
    def hasRemoveNaNRows(self):  
        return self.rFilter_remove_nan
    
    def hasRemoveNaNColumns(self):  
        return self.cFilter_remove_nan
    
    def hasRemove_SameVal_Columns(self):  
        return self.cFilter_remove_same_val   
        
     
    def getFeatures(self):  
        return self.features
    
    
    def getCloseIndex(self):  
        return self.closeIndex
    
    def getHighIndex(self):  
        return self.highIndex
    
    def getLowIndex(self):  
        return self.lowIndex
    
    def getVolumeIndex(self):  
        return self.volumeIndex
    
    def getOpenIndex(self):
        return self.openIndex
    

'''
Created on 10-May-2017

@author: fly
'''

import numpy as np
from sklearn.preprocessing import MinMaxScaler

class StockInput(object):
    '''
    classdocs
    '''


    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.fileName=fileName
        self.scaler = MinMaxScaler(feature_range=(0, 100))
        self.transform = self.scaler.fit_transform
        self.inversetransform =self.scaler.inverse_transform
    
       
    
    def load_data(self):
        dataSet =  np.genfromtxt(self.fileName, delimiter=",", skip_header=True)
        return dataSet[:, 0:dataSet.shape[1]] 
    
    def transform(self,data):
        return self.transform(data)
    
    def inverseTransform(self,data):
        return self.inversetransform(data)
       
    def getXY(self,ndArray,YindexArry):        
        yvalue = ndArray[:, YindexArry]        
        return np.delete(ndArray.copy(), (-1), axis=0), np.delete(yvalue.copy(), (0), axis=0)

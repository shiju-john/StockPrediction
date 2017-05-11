'''
Created on 10-May-2017

@author: fly
'''

import StockModel
import StockInput
import ConfigReader
import os.path
import numpy as np

def processData(rows):
    
    for row in rows:
        
               
        exchangeId,stockName,timeDelay,days,companyName = row[0:5]
        fileName = exchangeId+'_'+companyName
        filePath = "dataset/talib/{0}.csv".format(fileName)
        
        if(os.path.isfile(filePath) ):
            print ("start training Of stock" ,fileName)
            model = StockModel.StockModel()            
            stockInputObj = StockInput.StockInput(filePath)
            dataset = stockInputObj.load_data()
             
            trainX,trainY = stockInputObj.getXY(dataset,[2,3,4,6])
            trainX = stockInputObj.transform(trainX)
            trainY = stockInputObj.transform(trainY)
           
            testX = trainX[trainX.shape[0]-10::]            
            testY = trainY[trainY.shape[0]-10::]
            
            print(trainX.shape)
                       
            model.trainModel(trainX,trainY)      
            
            np.set_printoptions(formatter={'float':'{:0.2f}'.format})
        
            result = model.predictModel(testX,testY)
            print("Predicted result",stockInputObj.inverseTransform(result))
            print("Actual   Result",stockInputObj.inverseTransform(testY))
            
         
       


if __name__ == '__main__':    
    rows = ConfigReader.processCSVFile('config/inputConfig.csv')
    processData(rows)
    
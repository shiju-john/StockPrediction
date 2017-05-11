
'''
Created on 10-May-2017

@author: fly
predict the stock exchange value using the MultiOutputRegressor model
'''

from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor

class StockModel (object):

    def __init__(self) :
        # Build Model
        self.model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0))
        
    #Train model
    def trainModel(self,trainX,trainY):        
        self.model = self.model.fit(trainX, trainY)
      
    
    #Predict 
    def predictModel(self,testX,testY):        
        result = self.model.predict(testX)
        
        print(self.model.score(testX,testY)*100)
        return result
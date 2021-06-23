'''
Use Generated Models
Vidur Modgil
Basketball Reference Project

Use the generated models to create more efficiently running code than previous Models
'''

import pandas as pd
import os
import pathlib
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from joblib import load
from sklearn.linear_model import LinearRegression

class PotentialPredictions:
    def __init__(self):
        self.workingDir = pathlib.Path().absolute()
        self.dataSet = pd.read_csv(str(self.workingDir) + '/Basketball Info Dump.csv')
        self.reOrg = self.dataSet.reindex(sorted(self.dataSet.columns), axis=1)
        self.independentVariable = self.reOrg[list(self.reOrg.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Assists Per Game', 'Random Number', 'Max RPG', 'Max APG', 'Unnamed: 0']))].copy()
    
    def getPlayer(self, playerName):
        return self.dataSet.groupby('Player').get_group(playerName)

class Points(PotentialPredictions):
    
    def __init__(self):
        super().__init__()
        self.pointsModelLinear = load(str(self.workingDir) + '/Model Dumps/Points/Linear Regression Model.joblib')
        self.pointsModelQuadratic = load(str(self.workingDir) + '/Model Dumps/Points/Quadratic Model.joblib')
        self.pointsModelCubic = load(str(self.workingDir) + '/Model Dumps/Points/Cubic Model.joblib')
        self.pointsModelNB = load(str(self.workingDir) + '/Model Dumps/Points/Cubic Model.joblib')
        self.dependentVariable = self.dataSet['Max PPG']
        self.inputType = []
    
    def predict(self, modelType):
        didPass = True
        self.inputType.append(modelType)
        if modelType == 'Linear':
            self.predictions = self.pointsModelLinear.predict(self.independentVariable)
        elif modelType == 'Quadratic':
            self.predictions = self.pointsModelQuadratic.predict(self.independentVariable)
        elif modelType == 'Cubic':
            self.predictions = self.pointsModelCubic.predict(self.independentVariable)
        else:
            didPass = False
        if didPass == True:
            self.dataSet['Prediction Variable ' + modelType] = list(self.predictions)
        return didPass
        
    def scoreModel(self, modelType):
        self.dataSet['Max PPG']
        if modelType == 'Linear':
            return self.pointsModelLinear.score(self.independentVariable, self.dependentVariable)
        elif modelType == 'Quadratic':
            return self.pointsModelQuadratic.score(self.independentVariable, self.dependentVariable)
        elif modelType == 'Cubic':
            return self.pointsModelCubic.score(self.independentVariable, self.dependentVariable)
        else:
            return None

    def playerPredictionPoints(self, PlayerName):
        self.pointPredictions = []
        if len(self.inputType) == 0:
            return None
        else:
            playerStats = self.getPlayer(PlayerName)
            for inpt in self.inputType:
                self.pointPredictions.append(max(list(playerStats['Prediction Variable ' + inpt])))
            return self.pointPredictions[0]

def main():
    test = Points()
    test.predict('Linear')
    print(test.playerPredictionPoints('Joel Embiid'))

if __name__ == '__main__':
    main()
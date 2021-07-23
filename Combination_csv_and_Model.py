'''
Combining two different csvs and generating a model
Vidur Modgil
Basketball Reference Project-College Reference

Use 2 Different Scraped CSVs to generate pre-draft predicitons using college data
'''

# Imports
import os
import pandas as pd
from random import random as rand
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from joblib import dump

def main():
    workingDir = os.getcwd()
    # File path
    nbaCsvStorage = workingDir + '/Basketball Info Dump.csv'
    collegeCsvStorage = workingDir + '/College Basketball/College Stats.csv'
    
    # Reading csv from file into df
    nbaDfOriginal = pd.read_csv(nbaCsvStorage)
    collegeDf = pd.read_csv(collegeCsvStorage)
    nbaDf = nbaDfOriginal[['Max PPG', 'Max RPG', 'Max APG', 'Player']].copy()
    print(nbaDf)

    # Combining the dataframe
    collegePlayersUnique = set(collegeDf['Player'].copy())
    nbaPlayersUnique = set(nbaDf['Player'].copy())

    for player in nbaPlayersUnique:
        if player not in collegePlayersUnique:
           playerIndex = nbaDf[nbaDf['Player'] == player].index
           nbaDf.drop(playerIndex, inplace=True)
    nbaDf.set_index('Player', drop=True, inplace=True)
    nbaDf.drop_duplicates(inplace=True, ignore_index = False)
    
    # Imputating the missing calues
    collegeDf.set_index('Player', inplace=True)
    combinedDf = pd.concat([nbaDf, collegeDf], 1, 'inner')
    combinedDf.fillna(combinedDf.median(), inplace=True)
    combinedDf.dropna(axis=1, how='all', inplace=True)
    print(combinedDf.info())

    # Splitting the data randomly
    rows = len(combinedDf['Max PPG'])
    randomVal = [rand() for _ in range(rows)]
    combinedDf['Rand_Key'] = randomVal
    combinedDf.sort_values('Rand_Key', inplace=True, ignore_index=True)
    trainData = combinedDf[:1500]
    testData = combinedDf[1501:]

    # Model Generation
    indVar = trainData[combinedDf.columns.difference(['Max PPG', 'Max RPG', 'Max APG', 'Unnamed: 0', '* = NCAA Tournament appearance'])]
    depVar = trainData[['Max PPG', 'Max RPG', 'Max APG']]
    indVarTest = testData[combinedDf.columns.difference(['Max PPG', 'Max RPG', 'Max APG', 'Unnamed: 0', '* = NCAA Tournament appearance'])]
    depVarTest = testData[['Max PPG', 'Max RPG', 'Max APG']]

    linearRegrPoints = LinearRegression()
    linearRegrPoints.fit(indVar, depVar)
    print(linearRegrPoints.score(indVarTest, depVarTest))

    quadRegrPoints = make_pipeline(PolynomialFeatures(3), LinearRegression())
    quadRegrPoints.fit(indVar, depVar)
    print(quadRegrPoints.score(indVarTest, depVarTest))

    
    

if __name__ == '__main__':
    main()


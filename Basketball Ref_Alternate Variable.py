'''
Basketball Reference Usage 2021
Vidur Modgil
Use newfound pandas knowledge to yeet project into existence
'''

# Imports
from basketballRefCommands import BasketballReferencePull
import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.naive_bayes import GaussianNB

def PosToNumeric(position):
    if position == 'PG':
        return 1
    elif position == 'SG':
        return 2
    elif position == 'SF':
        return 3
    elif position == 'PF':
        return 4
    else:
        return 5

def main():
    pd.options.mode.chained_assignment = None
    # For Loop Gathers all season data from 1990-2020
    season_index = []
    for i in range(30):
        year = 1990 + i
        true_year = str(year)
        season = BasketballReferencePull('https://www.basketball-reference.com/leagues/NBA_' + true_year + '_per_game.html', true_year)
        season.rename(columns = {"Player" : "Player" + true_year})
        season_index.append(season)
    
    # Combines this data into 1 data drame
    seasons = pd.concat(season_index, axis = 0, ignore_index = True, join = 'inner')
    seasons.sort_values('Player', axis=0, inplace=True, ascending=True, ignore_index=True)
    seasons.drop(labels='Rank', inplace=True, axis=1)

    seasonsFloatable = seasons[seasons.columns.difference(['Player','Position','Team'])].apply(pd.to_numeric, errors='coerce', downcast='float', )   # Casts dataframe from str --> float
    
    seasons[seasonsFloatable.columns] = seasonsFloatable
    
    # Gets a Unique set of player names
    playerNames = set(seasons['Player'].copy())
    playerNames = list(playerNames)
    playerNames.sort()

    # Initializes Empty Lists to store new stats
    normalizedPPG = []

    # Groups player names together
    groupedSeasons = seasons.groupby('Player')

    # Iterates through each player group to generate stats
    for player in playerNames:
        sortedDf = groupedSeasons.get_group(player)     # Generates unique player data frame

        # Gets the stats from the data frame
        pointsPerGame = list(sortedDf['Points Per Game'].copy())

        # Finds the maximum of each stat and computes the new stats using that
        maxPpg = max(pointsPerGame)


        for year in pointsPerGame:
            normalizedPPG.append(maxPpg)
            
    
    seasons['Max PPG'] = normalizedPPG

    # Binning the Data
    seasons['Max_PPG_RANK'] = pd.qcut(seasons['Max PPG'], labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], q=10, precision=0)

    # Drop unwanted Quartiles to normalize the data
    droppedDeciles = (1, 2, 10)
    for decile in droppedDeciles:
        seasonsDeciles = seasons.groupby('Max_PPG_RANK')
        decileGroup = seasonsDeciles.get_group(decile)
        decileIndex = list(decileGroup.index)
        seasons.drop(decileIndex, inplace=True)


    # Changes str Categorical variables to numeric
    seasons['Position'] = seasons['Position'].apply(PosToNumeric)

    # Split Data into test data frames and model generation
    random.seed(42069)
    randomRowLabel = []
    for _ in range(len(pointsPerGame) - 1):
        randomNumber = random.random()
        randomRowLabel.append(randomNumber)
    seasons['Random Number'] = randomNumber
    seasons.sort_values('Random Number', ascending=True, ignore_index=True, inplace=True)
    trainData = seasons[0:10_000].copy()
    testData = pd.DataFrame(seasons[10_001:].copy())

    # Actual Model generations
    
    independentVariable = trainData[list(trainData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK']))]
    dependentVariable = trainData['Max PPG']
    
    # Linear Model Generation
    linearRegr = LinearRegression()
    linearRegr.fit(independentVariable, dependentVariable)
    testSet = testData[list(testData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK']))]
    trainSet = trainData[list(trainData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK']))]
    testPrediction = linearRegr.predict(testSet)
    trainPrediction = linearRegr.predict(trainSet)
    
    testData['PredictionVariable_Linear'] = testPrediction
    trainData['PredictionVariabl_Linear'] = trainPrediction

    print('Linear Regression r^2 value is: ')
    print(linearRegr.score(testSet, testData['Max PPG']))

    print('\nLinear Regression r^2 values(train data) is: ')
    print(linearRegr.score(trainSet, trainData['Max PPG']))


if __name__ == '__main__':
    main()
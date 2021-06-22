'''
Basketball Reference Usage 2021
Vidur Modgil
Use newfound pandas knowledge to yeet project into existence
'''
# Test
# Imports
from basketballRefCommands import BasketballReferencePull
import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from joblib import dump

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
    for i in range(31):
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

    seasons.to_csv('/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Basketball Info Dump.csv')
    
    # Gets a Unique set of player names
    playerNames = set(seasons['Player'].copy())
    playerNames = list(playerNames)
    playerNames.sort()

    # Initializes Empty Lists to store new stats
    normalizedPPG = []
    normalizedRPG = []
    normalizedAPG = []

    # Groups player names together
    groupedSeasons = seasons.groupby('Player')

    # Iterates through each player group to generate stats
    for player in playerNames:
        sortedDf = groupedSeasons.get_group(player)     # Generates unique player data frame

        # Gets the stats from the data frame
        pointsPerGame = list(sortedDf['Points Per Game'].copy())
        reboundsPerGame = list(sortedDf['Total Rebounds Per Game'].copy())
        assistsPerGame = list(sortedDf['Assists Per Game'].copy())

        maxPpg = max(pointsPerGame)
        maxRpg = max(reboundsPerGame)
        maxApg = max(assistsPerGame)


        for _ in pointsPerGame:
            normalizedPPG.append(maxPpg)
            normalizedRPG.append(maxRpg)
            normalizedAPG.append(maxApg)
            
    
    seasons['Max PPG'] = normalizedPPG
    seasons['Max RPG'] = normalizedRPG
    seasons['Max APG'] = normalizedAPG

    # Binning the Data
    categories = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    seasons['Max_PPG_RANK'] = pd.qcut(seasons['Max PPG'], labels=categories, q=10, precision=0)
    seasons['Max_RPG_RANK'] = pd.qcut(seasons['Max RPG'], labels=categories, q=10, precision=0)
    seasons['Max_APG_RANK'] = pd.qcut(seasons['Max APG'], labels=categories, q=10, precision=0)

    # Changes str Categorical variables to numeric
    seasons['Position'] = seasons['Position'].apply(PosToNumeric)

    # Split Data into test data frames and model generation
    random.seed(123456)
    randomRowLabel = []
    for _ in range(len(pointsPerGame) - 1):
        randomNumber = random.random()
        randomRowLabel.append(randomNumber)
    seasons['Random Number'] = randomNumber
    seasons.sort_values('Random Number', ascending=True, ignore_index=True, inplace=True)
    trainData = seasons[0:10_000].copy()
    testData = pd.DataFrame(seasons[10_001:].copy())

    # Actual Model generation
    
    independentVariable = trainData[list(trainData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK', 'Points Per Game', 'Total Rebounds Per Game', 'Assists Per Game', 'Random Number', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Assists Per Game', 'Max RPG', 'Max APG']))]
    dependentVariablePoints = trainData['Max PPG']
    dependentVariableRebounds = trainData['Max RPG']
    dependentVariableAssists = trainData['Max APG']
    
    # Linear Model Generation
    linearRegrPoints = LinearRegression()
    linearRegrRebounds = LinearRegression()
    linearRegrAssists = LinearRegression()
    # Fits x and y variable to linear model
    linearRegrPoints.fit(independentVariable, dependentVariablePoints)
    linearRegrRebounds.fit(independentVariable, dependentVariableRebounds)
    linearRegrAssists.fit(independentVariable, dependentVariableAssists)
    
    # Excludes unnesescary numbers
    testSet = testData[list(testData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK', 'Points Per Game', 'Total Rebounds Per Game', 'Assists Per Game', 'Random Number', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Assists Per Game', 'Max RPG', 'Max APG']))]
    trainSet = trainData[list(trainData.columns.difference(['Player', 'Max PPG', 'Team', 'Field Goal Percentage', '3-Point Field Goal Percentage', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', 'Free Throw Percentage', 'Max_PPG_RANK', 'Points Per Game', 'Total Rebounds Per Game', 'Assists Per Game', 'Random Number', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Assists Per Game', 'Max RPG', 'Max APG']))]

    # Uses linear model to predict
    testPredictionPoints = linearRegrPoints.predict(testSet)
    trainPredictionPoints = linearRegrPoints.predict(trainSet)
    testPredictionRebounds = linearRegrRebounds.predict(testSet)
    trainPredictionRebounds = linearRegrRebounds.predict(trainSet)
    testPredictionAssists = linearRegrAssists.predict(testSet)
    trainPredictionAssists = linearRegrAssists.predict(trainSet)
    
    # Adds columns to dataframes
    testData['PredictionVariable_Linear_Points'] = testPredictionPoints
    trainData['PredictionVariable_Linear_Points'] = trainPredictionPoints
    testData['PredictionVariable_Linear_Rebounds'] = testPredictionRebounds
    trainData['PredictionVariable_Linear_Rebounds'] = trainPredictionRebounds
    testData['PredictionVariable_Linear_Assists'] = testPredictionAssists
    trainData['PredictionVariable_Linear_Assits'] = trainPredictionAssists


    # Finds the r^2 value of the model on the test data
    print('Linear Regression r^2 value(test data) is: ')
    print(linearRegrPoints.score(testSet, testData['Max PPG']))
    print(linearRegrRebounds.score(testSet, testData['Max RPG']))
    print(linearRegrAssists.score(testSet, testData['Max APG']))

    # Finds the r^2 value of the model on the train data
    print('\nLinear Regression r^2 values(train data) is: ')
    print(linearRegrPoints.score(trainSet, trainData['Max PPG']))
    print(linearRegrRebounds.score(trainSet, trainData['Max RPG']))
    print(linearRegrAssists.score(trainSet, trainData['Max APG']))

    # Output data for Joel Embiid
    wantedValues = testData[['PredictionVariable_Linear_Points', 'Max PPG', 'Player', 'Points Per Game']].copy().groupby('Player')
    print(wantedValues.get_group('Joel Embiid'))

    # Polynomial Regression
    # Fits a second degree polynomial to the data
    degree = 2
    polyregPoints = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    polyregRebounds = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    polyregAssists = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    polycubePoints = make_pipeline(PolynomialFeatures(3), LinearRegression())
    polycubeRebounds = make_pipeline(PolynomialFeatures(3), LinearRegression())
    polycubeAssists = make_pipeline(PolynomialFeatures(3), LinearRegression())
    
    polyregPoints.fit(independentVariable, dependentVariablePoints)
    polyregRebounds.fit(independentVariable, dependentVariableRebounds)
    polyregAssists.fit(independentVariable, dependentVariableAssists)
    polycubePoints.fit(independentVariable, dependentVariablePoints)
    polycubeRebounds.fit(independentVariable, dependentVariableRebounds)
    polycubeAssists.fit(independentVariable, dependentVariableAssists)


    # Scoring of the data
    print('\nPolynomial Regression r^2 value(test data, quadratic) is:')
    print(polyregPoints.score(testSet, testData['Max PPG']))
    print(polyregRebounds.score(testSet, testData['Max RPG']))
    print(polyregAssists.score(testSet, testData['Max APG']))

    print('\nPolynomial Regression r^2 value(test data, cubic) is:')
    print(polycubePoints.score(testSet, testData['Max PPG']))
    print(polycubeRebounds.score(testSet, testData['Max RPG']))
    print(polycubeAssists.score(testSet, testData['Max APG']))
    
    # Predicts the test data
    polynomialPredictionQuad = list(polyregPoints.predict(testSet))
    polynomialImputationQuad = list(polyregPoints.predict(trainSet))
    polynomialPredictionCubic = list(polycubePoints.predict(testSet))
    polynomialImputationCubic = list(polycubePoints.predict(trainSet))
    
    # Put into dataframe
    testData['Polynomial Prediction(Quad)_Points'] = polynomialPredictionQuad
    trainData['Polynomial Prediction(Quad)_Points'] = polynomialImputationQuad
    testData['Polynomial Prediction(cubic)_Points'] = polynomialPredictionCubic
    trainData['Polynomial Prediction(cubic)_Points'] = polynomialImputationCubic

    # Naive Bayes Classifier
    gnbClassifierPoints = GaussianNB()
    gnbClassifierPoints.fit(independentVariable, trainData['Max_PPG_RANK'])
    gnbPredictedRow = list(gnbClassifierPoints.predict(testSet))
    testData['GaussianNB_Points'] = gnbPredictedRow
    print(testData[['Max PPG', 'PredictionVariable_Linear_Points', 'Polynomial Prediction(Quad)_Points', 'Polynomial Prediction(cubic)_Points', 'GaussianNB_Points', 'Max_PPG_RANK']])

    # Creating Pickle Dump Files
    dump(linearRegrPoints, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Linear Regression Model.joblib')
    dump(polyregPoints, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Quadratic Model.joblib')
    dump(polycubePoints, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Cubic Model.joblib')
    dump(gnbClassifierPoints, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Gaussian Naive Bayes Model.joblib')

    dump(linearRegrRebounds, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Linear Regression Model_Rebounds.joblib')
    dump(polyregRebounds, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Quadratic Model_Rebounds.joblib')
    dump(polycubeRebounds, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Cubic Model_Rebounds.joblib')
    
    dump(linearRegrAssists, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Linear Regression Model_Assists.joblib')
    dump(polyregAssists, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Quadratic Model_Assists.joblib')
    dump(polycubeAssists, '/Users/vidurmodgil/Desktop/Programming Projects/BasketBall Reference Analysis/Basketball-Reference-Web-Scraping/Model Dumps/Cubic Model_Assists.joblib')

    groupedTestData = None
    try:
        groupedTestData = trainData.groupby('Player').get_group('Kyle Korver')
    except:
        groupedTestData = testData.groupby('Player').get_group('Kyle Korver')
    print(groupedTestData[['Max PPG', 'PredictionVariable_Linear_Points', 'Polynomial Prediction(Quad)_Points', 'Polynomial Prediction(cubic)_Points']])

if __name__ == '__main__':
    main()
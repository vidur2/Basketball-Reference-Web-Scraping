'''
Combining two different csvs and generating a model
Vidur Modgil
Basketball Reference Project-College Reference

Use 2 Different Scraped CSVs to generate pre-draft predicitons using college data
'''

# Imports
import os
import pandas as pd
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
    

if __name__ == '__main__':
    main()


'''
Combining two different csvs and generating a model
Basketball Reference Code-College Reference
7/21/21
'''

# Imports
import os
import pandas as pd

def main():
    workingDir = os.getcwd()
    # File path
    nbaCsvStorage = workingDir + '/Basketball Info Dump.csv'
    collegeCsvStorage = workingDir + '/College Basketball/College Stats.csv'
    
    # Reading csv from file into df
    nbaDf = pd.read_csv(nbaCsvStorage)
    collegeDf = pd.read_csv(collegeCsvStorage)
    print(nbaDf)

    # Combining the dataframe
    collegePlayersUnique = set(collegeDf['Player'].copy())
    nbaPlayersUnique = set(nbaDf['Player'].copy())

    for player in nbaPlayersUnique:
        if player not in collegePlayersUnique:
           playerIndex = nbaDf[nbaDf['Player'] == player].index
           nbaDf.drop(playerIndex, inplace=True)
    
    print(nbaDf)

if __name__ == '__main__':
    main()


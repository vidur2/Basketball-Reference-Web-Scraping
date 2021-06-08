'''
Basketball Reference Usage 2021
Vidur Modgil
Use newfound pandas knowledge to yeet project into existence
'''

# Imports
from basketballRefCommands import BasketballReferencePull
import pandas as pd


def main():
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

    seasonsFloatable = seasons[seasons.columns.difference(['Player','Position','Team'])].apply(pd.to_numeric, errors='coerce', downcast='float')   # Casts dataframe from str --> float
    
    seasons[seasonsFloatable.columns] = seasonsFloatable
    
    # Gets a Unique set of player names
    playerNames = set(seasons['Player'].copy())
    playerNames = list(playerNames)
    playerNames.sort()

    # Initializes Empty Lists to store new stats
    normalizedPPG = []
    normalizedRPG = []
    normalizedAPG = []
    normalizedBPG = []
    normalizedSPG = []
    averagedPotential = []

    # Groups player names together
    groupedSeasons = seasons.groupby('Player')

    # Iterates through each player group to generate stats
    for player in playerNames:
        sortedDf = groupedSeasons.get_group(player)     # Generates unique player data frame
        
        # Lists which are reset each iteration
        averagingPPG = []
        averagingRPG = []
        averagingAPG = []
        averagingBPG = []
        averagingSPG = []

        # Gets the stats from the data frame
        pointsPerGame = list(sortedDf['Points Per Game'].copy())
        reboundsPerGame = list(sortedDf['Total Rebounds Per Game'].copy())
        assistsPerGame = list(sortedDf['Assists Per Game'].copy())
        blocksPerGame = list(sortedDf['Blocks Per Game'].copy())
        stealsPerGame = list(sortedDf['Steals Per Game'].copy())

        # Finds the maximum of each stat and computes the new stats using that
        maxPpg = max(pointsPerGame)
        maxRpg = max(reboundsPerGame)
        maxApg = max(assistsPerGame)
        maxBpg = max(blocksPerGame)
        maxSpg = max(stealsPerGame)

        if maxPpg == 0:
            for _ in pointsPerGame:
                normalizedPPG.append(0)
                averagingPPG.append(0)
        else:
            for year in pointsPerGame:
                normalizedPPG.append((year/maxPpg) * 100)
                averagingPPG.append((year/maxPpg) * 100)
        
        if maxRpg == 0:
            for _ in reboundsPerGame:
                normalizedRPG.append(0)
                averagingRPG.append(0)
        else:
            for year in reboundsPerGame:
                normalizedRPG.append((year/maxRpg) * 100)
                averagingRPG.append((year/maxRpg) * 100)
        
        if maxApg == 0:
            for _ in assistsPerGame:
                normalizedAPG.append(0)
                averagingAPG.append(0)
        else:
            for year in assistsPerGame:
                normalizedAPG.append((year/maxApg) * 100)
                averagingAPG.append((year/maxApg) * 100)
        
        if maxBpg == 0:
            for _ in blocksPerGame:
                normalizedBPG.append(0)
                averagingBPG.append(0)
        else:
            for year in blocksPerGame:
                normalizedBPG.append((year/maxBpg) * 100)
                averagingBPG.append((year/maxBpg) * 100)

        if maxSpg == 0:
            for _ in stealsPerGame:
                normalizedSPG.append(0)
                averagingSPG.append(0)
        else:
            for year in stealsPerGame:
                normalizedSPG.append((year/maxSpg) * 100)
                averagingSPG.append((year/maxSpg) * 100)
        
        for i in range(len(averagingPPG)):
            average = (averagingPPG[i - 1] + averagingRPG[i - 1] + averagingAPG[i - 1] + averagingBPG[i - 1] + averagingSPG[i - 1]) / 5
            averagedPotential.append(average)
            
    
    # Appends to data frame
    seasons['Potential_PPG_PCT'] = normalizedPPG
    seasons['Potential_RPG_PCT'] = normalizedRPG
    seasons['Potential_APG_PCT'] = normalizedAPG
    seasons['Potential_BPG_PCT'] = normalizedBPG
    seasons['Potential_SPG_PCT'] = normalizedSPG
    seasons['Tot_Potential_PCT'] = averagedPotential

    # Prints out data frame for specific player to check
    groupedSeasons = seasons.groupby('Player')
    testDF = print(groupedSeasons.get_group('Paul George'))

if __name__ == '__main__':
    main()
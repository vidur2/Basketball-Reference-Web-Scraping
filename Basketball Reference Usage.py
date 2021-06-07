'''
Basketball Reference Usage 2021
Vidur Modgil
Use newfound pandas knowledge to yeet project into existence
'''

# Imports
from basketballRefCommands import *


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

        # Casts the stats from str --> float64
        floatPointsPerGame = []
        floatReboundsPerGame = []
        floatAssistsPerGame = []

        for year in pointsPerGame:
            floatPointsPerGame.append(float(year))
        
        for year in reboundsPerGame:
            floatReboundsPerGame.append(float(year))
        
        for year in assistsPerGame:
            floatAssistsPerGame.append(float(year))

        pointsPerGame = floatPointsPerGame
        reboundsPerGame = floatReboundsPerGame
        assistsPerGame = floatAssistsPerGame
        
        # Finds the maximum of each stat and computes the new stats using that
        maxPpg = max(pointsPerGame)
        maxRpg = max(reboundsPerGame)
        maxApg = max(assistsPerGame)

        if maxPpg == 0:
            for _ in pointsPerGame:
                normalizedPPG.append(0)
        else:
            for year in pointsPerGame:
                normalizedPPG.append((year/maxPpg) * 100)
        
        if maxRpg == 0:
            for _ in reboundsPerGame:
                normalizedRPG.append(0)
        else:
            for year in reboundsPerGame:
                normalizedRPG.append((year/maxRpg) * 100)
        
        if maxApg == 0:
            for _ in assistsPerGame:
                normalizedAPG.append(0)
        else:
            for year in assistsPerGame:
                normalizedAPG.append((year/maxApg) * 100)
    
    # Appends to data frame
    seasons['Potential_PPG_PCT'] = normalizedPPG
    seasons['Potential_RPG_PCT'] = normalizedRPG
    seasons['Potential_APG_PCT'] = normalizedAPG

    # Prints out data frame for specific player to check
    groupedSeasons = seasons.groupby('Player')
    print(groupedSeasons.get_group('Paul George'))

if __name__ == '__main__':
    main()
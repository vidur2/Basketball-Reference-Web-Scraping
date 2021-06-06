'''
Basketball Reference Usage 2021
Vidur Modgil
Use newfound pandas knowledge to yeet project into existence
'''

# Imports
from basketballRefCommands import *


def main():
    season_index = []
    for i in range(30):
        year = 1990 + i
        true_year = str(year)
        season = BasketballReferencePull('https://www.basketball-reference.com/leagues/NBA_' + true_year + '_per_game.html', true_year)
        season.rename(columns = {"Player" : "Player" + true_year})
        season_index.append(season)
    
    seasons = pd.concat(season_index, axis = 0, ignore_index = True, join = 'inner')
    seasons.sort_values('Player', axis=0, inplace=True, ascending=True, ignore_index=True)
    playerNames = set(seasons['Player'].copy())
    playerNames = list(playerNames)
  
    normalizedPPG = []
    normalizedRPG = []
    playerNames.sort()

    groupedSeasons = seasons.groupby('Player')

    for player in playerNames:
        sortedDf = groupedSeasons.get_group(player)
        
        pointsPerGame = list(sortedDf['Points Per Game'].copy())
        reboundsPerGame = list(sortedDf['Total Rebounds Per Game'].copy())
        floatPointsPerGame = []
        floatReboundsPerGame = []

        for year in pointsPerGame:
            floatPointsPerGame.append(float(year))
        
        for year in reboundsPerGame:
            floatReboundsPerGame.append(float(year))
        
        pointsPerGame = floatPointsPerGame
        reboundsPerGame = floatReboundsPerGame
        
        maxPpg = max(pointsPerGame)
        maxRpg = max(reboundsPerGame)

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
    
    seasons['Potential_PPG_PCT'] = normalizedPPG
    seasons['Potential_RPG_PCT'] = normalizedRPG
    groupedSeasons = seasons.groupby('Player')
    print(groupedSeasons.get_group('Paul George'))

if __name__ == '__main__':
    main()
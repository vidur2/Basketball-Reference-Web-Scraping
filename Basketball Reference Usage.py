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
    groupedSeasons = seasons.groupby('Player')
    playerNames = list(playerNames)
    normalizedPPG = []
    playerNames.sort()
    for player in playerNames:
        sortedDf = groupedSeasons.get_group(player)
        
        pointsPerGame = list(sortedDf['Points Per Game'].copy())
        floatPointsPerGame = []

        for year in pointsPerGame:
            floatPointsPerGame.append(float(year))
        maxPpg = max(floatPointsPerGame)
        if maxPpg == 0:
            for _ in floatPointsPerGame:
                normalizedPPG.append(0)
        else:
            for year in floatPointsPerGame:
                normalizedPPG.append((year/maxPpg) * 100)
    seasons['RankedPPG'] = normalizedPPG
    statistics = list(seasons.columns)
    statistics.remove('Rank')
    statistics.remove('Player')
    statistics.remove('Position')
    statistics.remove('Team')
    for stat in statistics:
        pd.to_numeric(seasons[stat], downcast="float")
    groupedSeasons = seasons.groupby('Player')
    print(groupedSeasons.get_group('Paul George'))

if __name__ == '__main__':
    main()
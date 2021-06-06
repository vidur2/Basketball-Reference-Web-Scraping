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
    seasons.sort_values('Player', inplace=True)
    playerNames = set(seasons['Player'].copy())
    groupedSeasons = seasons.groupby('Player')
    sortedDf = groupedSeasons.get_group('Paul Pierce*')
    sortedDf.sort_values("Player's age on February 1 of the season",inplace=True)
    print(list(sortedDf["Player's age on February 1 of the season"].copy()))
    pointsPerGame = list(sortedDf['Points Per Game'].copy())
    maxPpg = max(int(pointsPerGame))
    normalizedPPG = []
    for year in pointsPerGame:
        normalizedPPG.append((int(year)/maxPpg) * 100)
    sortedDf['NormalizedPPG'] = normalizedPPG
    print(sortedDf)

if __name__ == '__main__':
    main()
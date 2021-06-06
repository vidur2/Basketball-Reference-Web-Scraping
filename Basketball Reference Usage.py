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
    seasons.sort_values("Player", ascending=True)
    print(seasons)

if __name__ == '__main__':
    main()
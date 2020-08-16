
# coding: utf-8

# In[3]:

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


# In[4]:

hyperlink = input('URL(From a Sports Reference Site): ')
player_name = input('Player Name: ')


# In[5]:

def BasketballReferencePull(link, year):
    #Gets and opens URL
    url = link
    page = requests.get(url)
    #Creates variable to alllow for extraction of data through beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')
    #Create lists to store data collected in for loops
    data_list = []
    header_list = []
    names_list = []
    #Collects headers from table on website
    for head in soup.find_all('th'):
        table_headers = head.get('aria-label')
        header_list.append(table_headers)
    del header_list[30:]
    #Collects data from table on website
    for table in soup.find_all('td'):
        table_data = table.get_text()
        data_list.append(table_data)
    #Generates index based
    cycles = 0
    for count in soup.find_all('td'):
        cycles = cycles + 1
    sort_method = []
    true_cycle = int(cycles/29)
    for i in range(true_cycle):
        for j in range(29):
            index = i
            sort_method.append(index)
    #Creates Dictionary out of Existing Data and Index Sorting Method
    d = {year :data_list, 'Sort_Method':sort_method}
    #Creates DataFrame out of Dictionary
    df = pd.DataFrame(d)
    #Sorts based on generated index from the for loop
    df = (df.set_index(['Sort_Method',df.groupby('Sort_Method').cumcount()])[year]
            .unstack()
            .add_prefix('value')
            .reset_index())
    #Sets the headers taken from the website as the headers for the pandas DataFrame
    df.columns = header_list
    #Drops unwanted columns
    df2 = df.drop(["Position", 'Team', 'Games', 'Games Started', 'Minutes Played Per Game', 'Field Goals Per Game', 'Field Goal Attempts Per Game', 'Field Goal Percentage', 'Rank', '3-Point Field Goals Per Game', '3-Point Field Goal Attempts Per Game', '2-Point Field Goals Per Game', '2-Point Field Goal Attempts Per Game', '2-Point Field Goal Percentage', 'Effective Field Goal Percentage', '3-Point Field Goal Percentage', 'Free Throw Attempts Per Game', 'Free Throws Per Game', 'Free Throw Percentage', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Total Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game', 'Turnovers Per Game', 'Personal Fouls Per Game'], axis = 1)
    df2.set_index('Player')
    return(df2)


# In[6]:

def BasketballReferencePlayer(link, player):
    #Gets and opens URL
    url = link
    page = requests.get(url)
    #Creates variable to alllow for extraction of data through beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')
    #Create lists to store data collected in for loops
    data_list = []
    header_list = []
    names_list = []
    #Collects headers from table on website
    for head in soup.find_all('th'):
        table_headers = head.get('aria-label')
        header_list.append(table_headers)
    del header_list[30:]
    #Collects data from table on website
    for table in soup.find_all('td'):
        table_data = table.get_text()
        data_list.append(table_data)
    #Generates index based
    cycles = 0
    for count in soup.find_all('td'):
        cycles = cycles + 1
    sort_method = []
    true_cycle = int(cycles/29)
    for i in range(true_cycle):
        for j in range(29):
            index = i
            sort_method.append(index)
    #Creates Dictionary out of Existing Data and Index Sorting Method
    d = {player :data_list, 'Sort_Method':sort_method}
    #Creates DataFrame out of Dictionary
    df = pd.DataFrame(d)
    #Sorts based on generated index from the for loop
    df = (df.set_index(['Sort_Method',df.groupby('Sort_Method').cumcount()])[player]
            .unstack()
            .add_prefix('value')
            .reset_index())
    #Sets the headers taken from the website as the headers for the pandas DataFrame
    df.columns = header_list
    return(df)


# In[7]:

BasketballReferencePlayer(hyperlink, player_name)


# In[8]:

Season_2017 = BasketballReferencePull('https://www.basketball-reference.com/leagues/NBA_2017_per_game.html', '2017')
Season_2017.set_index('Player')
Season_2017


# In[10]:

season_index = []
#Attempts to create a table based on ppg over seasons since 1990
for i in range(30):
    year = 1990 + i
    true_year = str(year)
    season = BasketballReferencePull('https://www.basketball-reference.com/leagues/NBA_' + true_year + '_per_game.html', true_year)
    season.rename(columns = {"Player" : "Player" + true_year})
    season_index.append(season)


# In[11]:

seasons = pd.concat(season_index, axis = 1, ignore_index = False, join = 'inner')
seasons


# In[66]:

age = (seasons["Player's age on February 1 of the season"] == 23)


# In[68]:

age


# In[ ]:




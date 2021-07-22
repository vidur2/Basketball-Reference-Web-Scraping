
# coding: utf-8

# In[3]:
'''
Scrape Basketball-Reference
Vidur Modgil
Basketball Reference Project- NBA Models

Use Requests and bs4 to scrape and organize data from basketball reference
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd


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
    return df


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




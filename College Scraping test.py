'''
Testing the viability of scraping college websites

Takes the set() of nba players from the .csv file
'''

# Imported Modules
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor


def getPlayerInfo(playerName: str):
    playerName = playerName.split(' ')
    firstName = playerName[0].lower()
    lastName = playerName[1].lower()
    #print('http://www.sports-reference.com/cbb/players/' + firstName + '-' + lastName + '-1.html')
    resp = requests.get('https://www.sports-reference.com/cbb/players/' + firstName + '-' + lastName + '-1.html')
    print(resp.status_code)
    if resp.status_code == 200:
        return resp.content

def main():
    workingDir = os.getcwd()
    csvData = pd.read_csv(workingDir + "/Basketball Info Dump.csv")
    nbaPlayers = set(csvData['Player'])
    myList = list()
    with ThreadPoolExecutor() as executor:
        pages = list()
        pageSubmission = [executor.submit(getPlayerInfo, player) for player in nbaPlayers]
        
        for page in concurrent.futures.as_completed(pageSubmission):
            pages.append(page.result())

if __name__ == '__main__':
    main()
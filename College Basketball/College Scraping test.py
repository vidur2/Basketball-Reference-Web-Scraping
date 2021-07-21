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
from concurrent.futures.process import ProcessPoolExecutor


def getPlayerInfo(playerName: str):
    try:
        playerName.replace('*', '')
        playerNameUnsplit = playerName
        playerName = playerName.split(' ')
        firstName = playerName[0].lower()
        lastName = playerName[1].lower()
        print('http://www.sports-reference.com/cbb/players/' + firstName + '-' + lastName + '-1.html')
        resp = requests.get('https://www.sports-reference.com/cbb/players/' + firstName + '-' + lastName + '-1.html')
        #print(resp.status_code)
        if resp.status_code == 200:
            return resp.content, playerNameUnsplit
    except Exception as e:
        print(str(e))

def storePlayerInfo(playerContent: tuple):
    try:
        if playerContent != None:
            htmlContent, playerName = playerContent
            soup = BeautifulSoup(htmlContent, 'html.parser')
            dataStorage = []
            headers = []
            #print(soup.prettify())
            for data in soup.find_all('td'):
                dataStorage.append(data.get_text())
            for title in soup.find_all('th'):
                headers.append(title.get('aria-label'))
            headers = headers[1:]

            while None in headers:
                headers.remove(None)
            college = dataStorage[0]
            iterator = 0
            indexStore = list()
            for element in dataStorage:
                if element == college:
                    indexStore.append(iterator)
                iterator = iterator + 1
            finalIndex = indexStore[len(indexStore) - 1]
            collegeCareerStats = dataStorage[finalIndex:]
            collegeCareerStats.insert(0, playerName)
            headers.insert(0,'Player' )
            df = pd.DataFrame(data=collegeCareerStats)
            df = df.transpose()
            df.columns = headers
            print(df)
            return df
            
    except Exception as e:
        print(str(e))


def main():
    workingDir = os.getcwd()
    workingDir.replace('/College Basketball', '')
    csvData = pd.read_csv(workingDir + "/Basketball Info Dump.csv")
    nbaPlayers = set(csvData['Player'])
    myList = list()
    print(len(nbaPlayers))

    with ThreadPoolExecutor() as executor:
        pages = list()
        pageSubmission = [executor.submit(getPlayerInfo, player) for player in nbaPlayers]
        
        for page in concurrent.futures.as_completed(pageSubmission):
            pages.append(page.result())
    
    with ProcessPoolExecutor() as executor:
        dfList = list()
        dfSubmission = [executor.submit(storePlayerInfo, player) for player in pages]

        for page in concurrent.futures.as_completed(dfSubmission):
            dfList.append(page.result())
    
    completedDf = pd.concat(dfList)
    completedDf.to_csv(workingDir + '/College Basketball/College Stats.csv')
    print(completedDf)


if __name__ == '__main__':
    main()
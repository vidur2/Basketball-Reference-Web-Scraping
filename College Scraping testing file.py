import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    page = requests.get('https://www.sports-reference.com/cbb/players/vince-carter-1.html')
    soup = BeautifulSoup(page.content, 'html.parser')
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
    print(len(headers))
    college = dataStorage[0]
    iterator = 0
    indexStore = list()
    for element in dataStorage:
        if element == college:
            indexStore.append(iterator)
        iterator = iterator + 1
    finalIndex = indexStore[len(indexStore) - 1]
    collegeCareerStats = dataStorage[finalIndex:]
    print(len(collegeCareerStats))
    df = pd.DataFrame(data=collegeCareerStats)
    df = df.transpose()
    df.columns = headers
    print(df)

if __name__ == '__main__':
    main()
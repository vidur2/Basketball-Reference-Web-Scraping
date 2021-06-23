# Basketball-Reference-Web-Scraping
## Overview
The purpose of this code is to take data from basketball reference and use it to make predictions.
Its current use is generating predictions about player potential(Max PPG, Max RPG, Max APG)
If you are using this code as a starter or otherwise please credit me

## Output
The model output is in the folder called 'Model Dumps.' The generation is done using the file called 'Basketball Ref Alternate.py.' The models are stored in .joblib files. The most accurate model currently is the Quadratic Regression ouput.

## The Code
### Gathering the data
The data is gathered from https://www.basketball-reference.com/. It is webscraped using the request and bs4 libraries. You can see the code in basketballRefCommands.py and the first for loop of 'Basketball Ref Alternate.py.' The data gathered is on every basketball player's seasons since 1990-Current Day.
### Storing the Data and Creating the target Variable
#### Storage
After Gathering the data, because it is so large, it is stored in a pandas dataframe. Because the years are split up by webpage, the dataframes are concacted into one large dataframe. 

#### Target Variable
The output of the model will be predicting the max PPG/RPG/APG output of a player based on the 20 other variables in use.
The target variable is not *directly* in the 23 variables scraped from basketball reference, so the code iterates through each player's stats and finds the max.

#### Model Training
In order to train the model, the data is split 10,000/7,491(along rows) with the 10,0000 being the train data and the 7941 being the test data.
The model is then fitted using sklearn's builtin tools with 20 variables as independent, and the Max PPG/RPG/APG as the dependent.

#### Model Testing
The model is tested on the remaining datapoints using [model_name].predict. The r^2 values are as follows:

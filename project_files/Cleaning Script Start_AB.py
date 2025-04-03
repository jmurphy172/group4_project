#Cleaning Script - Start
#AB 03/04/2025
#This script was created to serve as the start for the cleaning of the data we use in our data science project
#It contains steps for data import and preliminary exploration
#This script uses relative paths and assumes that the project folder is structured in this way:
#-project_folder/
#--data/
#---file.csv
#--script

#Loading required packages:
import pandas as pd
import numpy as np

#File import & basic descriptions
df = pd.read_csv('data/chess_games.csv')

print('Data headers')
print (df.head())

print('Data formats: ')
print (df.dtypes)

print('Number of records: ')
print(df.shape[0] - 1)

#Selecting relevant rows, renaming columns, dropping empty lines
df_project = df[['Event', 'White', 'Black', 'Result', 'WhiteElo',
                 'BlackElo', 'WhiteRatingDiff', 'BlackRatingDiff',
                 'ECO', 'Opening', 'Termination']]
df_project = df_project.rename (columns = {
    'Event': 'Game Type',
    'ECO': 'Opening ECO code'})
print(df_project.head())

#Data cleaning
#1. Removing empty rows
df_project_1 = df_project.dropna(axis=0, how='any')

#2. Selecting classical games
df_project_2 = df_project_1[df_project_1['Game Type'].str.contains('Classical', case=False, na=False)]
print(df_project_2.head())

#3. Dropping games that ended in a draw
df_project_3 = df_project_2[(df_project_2['Result'] != '1/2-1/2')]
print(df_project_3.head())


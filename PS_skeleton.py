#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pandorable problem set 3 for PSY 1210 - Fall 2019

@author: katherineduncan

In this problem set, you'll practice your new pandas data management skills, 
continuing to work with the 2018 IAT data used in class

Note that this is a group assignment. Please work in groups of ~4. You can divvy
up the questions between you, or better yet, work together on the questions to 
overcome potential hurdles 
"""
#Group Members
#Georgia Hadjis
#Joelle Girgis 
#Emily Schwartzman
#Youval Aberman
#William Staples
#%% import packages 
import os
import numpy as np
import pandas as pd

#%%
# Question 1: reading and cleaning

# read in the included IAT_2018.csv file
IAT=pd.read_csv('C:\\Users\\emily\\Documents\\GitHub\\Lec3_Files\\IAT_2018.csv',delimiter=',')

# rename and reorder the variables to the following (original name->new name):
# session_id->id
IAT=IAT.rename(columns={'session_id':'id'})
# genderidentity->gender
IAT=IAT.rename(columns={'genderidentity':'gender'})
# raceomb_002->race
IAT=IAT.rename(columns={'raceomb_002':'race'})
# edu->edu
IAT=IAT.rename(columns={'edu':'edu'})
# politicalid_7->politic
IAT=IAT.rename(columns={'politicalid_7':'politic'})
# STATE -> state
IAT=IAT.rename(columns={'STATE':'state'})
# att_7->attitude 
IAT=IAT.rename(columns={'att_7':'attitude'})
# tblacks_0to10-> tblack
IAT=IAT.rename(columns={'tblacks_0to10':'tblack'})
# twhites_0to10-> twhite
IAT=IAT.rename(columns={'twhites_0to10':'twhite'})
# labels->labels
IAT=IAT.rename(columns={'labels':'labels'})
# D_biep.White_Good_all->D_wIAhite_bias
IAT=IAT.rename(columns={'D_biep.White_Good_all':'D_white_bias'})
# Mn_RT_all_3467->rt
IAT=IAT.rename(columns={'Mn_RT_all_3467':'rt'})

IAT=IAT[['id','gender','race','edu','politic','state','attitude','tblack','twhite','labels','D_white_bias','rt']]

# remove all participants that have at least one missing value
IAT_clean = IAT.dropna(how='any',axis=0)

# check out the replace method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
# use this to recode gender so that 1=men and 2=women (instead of '[1]' and '[2]')
IAT_clean = IAT_clean.replace({'[1]':1,'[2]':2})

# use this cleaned dataframe to answer the following questions

#%%
# Question 2: sorting and indexing

# use sorting and indexing to print out the following information:

# the ids of the 5 participants with the fastest reaction times
rt_sort=IAT_clean.sort_values(by=['rt'])
print('\nFASTEST RTs:','\n',rt_sort.iloc[0:5,0])

# the ids of the 5 men with the strongest white-good bias
menbias_sort=IAT_clean.sort_values(by=['gender','D_white_bias'],ascending=[True,False])
print('\nMEN WITH STRONGEST BIAS','\n',menbias_sort.iloc[0:5,0])

# the ids of the 5 women in new york with the strongest white-good bias
ny=IAT_clean[IAT_clean.state=='NY']
womenbias_sort=ny.sort_values(by=['gender','D_white_bias'],ascending=[False,False])
print('\nNY WOMEN WITH STRONGEST BIAS','\n',womenbias_sort.iloc[0:5,0])

#%%
# Question 3: loops and pivots

# check out the unique method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html
# use it to get a list of states
states =pd.Series(pd.Categorical(IAT_clean.state)).unique()
# write a loop that iterates over states to calculate the median white-good
# bias per state
# store the results in a dataframe with 2 columns: state & bias



# now use the pivot_table function to calculate the same statistics
state_bias=...

# make another pivot_table that calculates median bias per state, separately 
# for each race (organized by columns)
state_race_bias=...

#%%
# Question 4: merging and more merging

# add a new variable that codes for whether or not a participant identifies as 
# black/African American
IAT_clean['race_black'] = 1*(IAT_clean.race==5)

# use your new variable along with the crosstab function to calculate the 
# proportion of each state's population that is black 
# *hint check out the normalization options
prop_black = (pd.crosstab(IAT_clean.race_black, IAT_clean.state))

prop_black_tran = prop_black.transpose() #easier view

print(pd.crosstab(IAT_clean.race_black, IAT_clean.state, normalize=True))
print(pd.crosstab(IAT_clean.race_black, IAT_clean.state, normalize='columns'))
print(pd.crosstab(IAT_clean.race_black, IAT_clean.state,  normalize='index')) 

# state_pop.xlsx contains census data from 2000 taken from http://www.censusscope.org/us/rank_race_blackafricanamerican.html
# the last column contains the proportion of residents who identify as 
# black/African American 
# read in this file and merge its contents with your prop_black table
census = pd.read_excel('state_pop.xlsx')
census=census.rename(columns={'State':'state'}) #consistency in 'state' column names, for merging

#merge census df with prop_black df --> HELP!
merged = pd.merge(census,prop_black_tran, on = ???????) #what is the matching identifier?
merged.describe()

# use the corr method to correlate the census proportions to the sample proportions

# now merge the census data with your state_race_bias pivot table

# use the corr method again to determine whether white_good biases is correlated 
# with the proportion of the population which is black across states
# calculate and print this correlation for white and black participants






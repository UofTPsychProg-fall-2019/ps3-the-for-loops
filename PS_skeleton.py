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
#edit, just to make it easier for folks 
localPath = '/Users/emily/Documents/GitHub/Lec3_Files/IAT_2018.csv'
IAT=pd.read_csv(localPath,delimiter=',')

# rename and reorder the variables to the following (original name->new name):
IAT.columns
IAT=IAT.rename(columns={'session_id':'id',      # session_id->id
                        'genderidentity':'gender',  #  genderidentity->gender
                        'raceomb_002':'race', #     raceomb_002->race
                        'politicalid_7':'politic'   ,# politicalid_7->politic
                        'STATE':'state',#           STATE -> state
                        #edu is already named like that, no need to change it
                        'att_7':'attitude',         # att_7->attitude 
                        'tblacks_0to10':'tblack',# tblacks_0to10-> tblack
                        'twhites_0to10':'twhite',# twhites_0to10-> twhite
                        'labels':'labels',       # labels->labels
                        'D_biep.White_Good_all':'D_white_bias',# D_biep.White_Good_all->D_white_bias
                        'Mn_RT_all_3467':'rt'})# Mn_RT_all_3467->rt

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
print('\nFASTEST RTs: ','\n',rt_sort.iloc[0:5,[0,11]])

# the ids of the 5 men with the strongest white-good bias
#first subset men. then apply sort_values method on that dataset.
menbias_sort=IAT_clean[(IAT_clean.gender==1)].sort_values(by=['D_white_bias'],ascending=[False])

print('\nMEN WITH STRONGEST BIAS','\n',menbias_sort.iloc[0:5,[0,10]])

# the ids of the 5 women in new york with the strongest white-good bias
ny=IAT_clean[IAT_clean.state=='NY']
womenbias_sort=ny[(ny.gender==2)].sort_values(by=['D_white_bias'],ascending=[False])
print('\nNY WOMEN WITH STRONGEST BIAS','\n',womenbias_sort.iloc[0:5,[0,10]])

#%%
# Question 3: loops and pivots

# check out the unique method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html
# use it to get a list of states
states=pd.unique(IAT_clean.state)

# write a loop that iterates over states to calculate the median white-good
# bias per state
# store the results in a dataframe with 2 columns: state & bias
df_state_bias = pd.DataFrame(columns=['state','bias'])
for state in states:
    s = IAT_clean[IAT_clean.state == state]
    median = s.D_white_bias.median()
    df_state_bias = df_state_bias.append({'state': state, 'bias': median}, ignore_index = True)

# now use the pivot_table function to calculate the same statistics
state_bias=pd.pivot_table (IAT_clean, values = 'D_white_bias',
                           index = ['state'],
                           aggfunc=np.median)
# make another pivot_table that calculates median bias per state, separately 
# for each race (organized by columns)
state_race_bias=pd.pivot_table(IAT_clean, values = 'D_white_bias',
                               index = ['state'],
                               columns = ['race'],
                               aggfunc=np.median)

#%%
# Question 4: merging and more merging

# add a new variable that codes for whether or not a participant identifies as 
# black/African American
IAT_clean['race_black'] = 1*(IAT_clean.race==5)
# use your new variable along with the crosstab function to calculate the 
# proportion of each state's population that is black 
# *hint check out the normalization options
prop_black = pd.crosstab(IAT_clean.state, IAT_clean.race_black, normalize='index')

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
#because by calling.loc [:,1] - you extract one column, so pandas saves the new object as an array. 
#so instead I just remove the 0 column from that dataframe
prop_black_True = prop_black.loc[:,1]  #index only column with black proportions
prop_black_True = prop_black.drop(0,axis=1)  #drop the columns named "0", on the vertical axis
prop_black_True = prop_black_True.rename(columns={1:'prop_black'}) #rename 

merged = pd.merge(prop_black_True, census, on= 'state')
merged.describe()

# use the corr method to correlate the census proportions to the sample proportions
np.corrcoef(merged.per_black,merged.prop_black)

# now merge the census data with your state_race_bias pivot table
merged2 = pd.merge(merged,state_bias,on='state')

# use the corr method again to determine whether white_good biases is correlated 
# with the proportion of the population which is black across states
np.corrcoef(merged2.prop_black,merged2.D_white_bias)

# calculate and print this correlation for white and black participants

corr_white = np.corrcoef(merged2.per_black, merged2.iloc[:,9])
corr_black = np.corrcoef(merged2.per_black, merged2.iloc[:,8])

print('\nWhite Correlation: {:.3f}'.format(corr_white[0,1]))
print('\nBlack Correlation: {:.3f}'.format(corr_black[0,1]))
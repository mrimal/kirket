# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:55:56 2018

@author: mpr

I'll start by using the csv files generated, as fetching the data again
and again gets a tad bit annoying.

Once the thing is final, we can remove this block of code to read the final 
pandas dataframe generated in the ball_by_ball.py file to be the main source of
data.

#TODO:
#Actual graphing. 
#Additionally an automated system to type a player's name and 
#lookup the player numbers rather than creating a dictionary 
#would be ideal.

"""

import pandas as pd
import glob

path = 'playerdata/*.csv'

def cumalative_runs(filedirectory):
    main_df = pd.DataFrame()
    
    for each in glob.iglob(filedirectory):
        df = pd.read_csv(each, index_col=None, header=0)
        filename = each.replace('playerdata/','')
        filename = filename.replace('.csv','')
        df['cumal_runs'] = df['mean_runs'].cumsum()
        df['batsman'] = filename
        main_df = main_df.append(df)
        
    main_df = main_df.drop('Unnamed: 0', axis=1)
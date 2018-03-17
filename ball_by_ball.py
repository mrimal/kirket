# -*- coding: utf-8 -*-
"""
@author: 
    
    Cricinfo does not have an API from where data can be easily extracted. 
    Data here is extracted using the wagon wheel json dump from cricinfo's 
    website which I saw Github user rishiriv doing in his Cricket cronjob. 
    
"""

import requests
import json
import pandas as pd
#import numpy as np
import os 
import datapull

batsman_id = {'ViratKohli':'253802','JoeRoot':'303669','ABDV':'44936',
              'KaneWilliamson':'277906','StevenSmith':'267192'}

def ball_by_ball(career_matches, player_number):
    final_frame = pd.DataFrame()
    for game_id in career_matches:
    	
        innings1 = requests.get('http://www.espncricinfo.com/ci/engine/match/gfx/%s.json?inning=1;template=wagon'%(game_id))
        innings2 = requests.get('http://www.espncricinfo.com/ci/engine/match/gfx/%s.json?inning=2;template=wagon'%(game_id))
                
        data_dict = json.loads(innings1.content)
        data_dict2 = json.loads(innings2.content)    
        df = pd.DataFrame(data_dict)
        df2 = pd.DataFrame(data_dict2)
        df['inning'] = 1
        df2['inning'] = 2
        
        df = df.append(df2)
        
        del df2 
        
        def f(i):
            return i['bat'], i['bowl'], i['o_u'], i['ovr'], i['r'], i['r_t']
            
        df['batsman'], df['bowler'], df['ball_num'], df['ovr'], df['runs_batter'], df['runs_w_extras'] = zip(*df.runs.apply(f))
        
        for param in ['ovr', 'runs_batter', 'runs_w_extras']:
            df[param] = df[param].astype(float)    
            
        df = df.drop('runs', axis=1)
        
        df = df[df['batsman'] == player_number]
        
        df = df.reset_index(drop=True)
        
        df['ball_no'] = df.index + 1
    
        final_frame = final_frame.append(df)
        
    ball_by = final_frame.groupby('ball_no').aggregate({'ball_no':'size','runs_batter':'mean'}).rename(columns={'ball_no':'total_innings', 'runs_batter':'mean_runs'}).reset_index()
    return ball_by
   


try:
    os.stat("playerdata")
except:
    os.mkdir("playerdata")

# Now looping over the batsman's names to get their full career info and then 
# getting the list of matches plus the scores
final_dataset = pd.DataFrame()

for key, value in batsman_id.iteritems():
    career_matches = datapull.find_player_matches(value)
    career_runs = ball_by_ball(career_matches, value)
    final_dataset = final_dataset.append(career_runs)
    print(career_runs)
    filename = os.path.join("playerdata", key)
    filename = filename + ".csv"
    career_runs.to_csv(filename, encoding='utf-8')

#TODO:
#Actual graphing. 
#Additionally an automated system to type a player's name and 
#lookup the player numbers rather than creating a dictionary 
#would be ideal.

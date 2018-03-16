# -*- coding: utf-8 -*-
"""

@author: mpr

"""

#Currently trying it out with Joe Root's debut match. Can extend it to the 
#full list once we have the wrapper up and running.

import requests
from bs4 import BeautifulSoup
import re

# Virat Kohli - 253802
# Joe Root = 303669
# ABDV = 44936
# Kane Williamson= 277906
# Steven Smith = 267192
##First let us find all the games a player has played.

def find_player_matches(playerid):
    """
    Finds the list of ODI innings the batsman has played, 
    and finds the match numbers and returns it as a list.
    """
    page = requests.get("http://stats.espncricinfo.com/ci/engine/player/"+playerid+".html?class=2;template=results;type=batting;view=innings")
    soup = BeautifulSoup(page.text)
    
    player_match_list = soup.find_all(name='a', attrs={"title":"view the scorecard for this row"})
    
    #From the above list we need to parse out the match numbers which are part of 
    #the link. part after the /match/ and before the .html
    
    match_list = []
    for each in player_match_list:
        a = str(each)
        b = re.sub('<a href="/ci/engine/match/', "", a)
        b = b.split(".")       
        match_list.append(b[0])
    return match_list
    

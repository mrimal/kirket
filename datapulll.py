# -*- coding: utf-8 -*-
"""

@author: mpr

TODO: 
    Joe Root :
        http://stats.espncricinfo.com/ci/engine/player/303669.html?class=2;template=results;type=batting;view=innings
    This is the list to pull from, from here pull the match numbers, and then the data dump.g
    
"""

#Currently trying it out with Joe Root's debut match. Can extend it to the 
#full list once we have the wrapper up and running.

import requests
import json
import pprint
from bs4 import BeautifulSoup
##First let us find all the games a player has played.

page = requests.get("http://stats.espncricinfo.com/ci/engine/player/303669.html?class=2;template=results;type=batting;view=innings")
soup = BeautifulSoup(page.text)

#game_list = soup.find_all('title="view the scorecard for this row"')

player_match_list = soup.find_all(name='a', attrs={"title":"view the scorecard for this row"})

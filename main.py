from bs4 import BeautifulSoup
import sqlite3
import re
from concurrent.futures import ThreadPoolExecutor
import os

import dominate
from dominate.tags import *
import lxml.etree
import lxml.builder 
import datetime

from dom_generator_helper import *
from pages.home import *
from pages.rt_history import *
from pages.rt_ffa_leaderboard import *
from pages.rt_teamer_leaderboard import *
from pages.rt_duel_leaderboard import *
from pages.rt_s5_history import *
from pages.rt_s5_ffa_leaderboard import *
from pages.rt_s5_teamer_leaderboard import *
from pages.rt_s5_duel_leaderboard import *
from pages.pbc_history import *
from pages.pbc_ffa_duel_leaderboard import *
from pages.pbc_combined_leaderboard import *
from pages.pbc_ffa_leaderboard import *
from pages.pbc_teamer_leaderboard import *
from pages.pbc_duel_leaderboard import *

menu_list = {
    'Home' : {
        'Home': {'name': 'Home', 'link': 'index.html'}
    },
    'Realtime' : {
        'Game History' : {'name': 'Real time Game History', 'link': 'rt_games.html'},
        'FFA Leaderboard' : {'name': 'Real time FFA Leaderboard', 'link': 'rt_ffa_leaderboard.html'},
        'Teamer Leaderboard' : {'name': 'Real time Teamer Leaderboard', 'link': 'rt_teamer_leaderboard.html'},
        'Duel Leaderboard' : {'name': 'Real time Duel Leaderboard', 'link': 'rt_duel_leaderboard.html'},       
    },
    'Season 5 Realtime' : {
        'Game History' : {'name': 'Season 5 Real time Game History', 'link': 'rt_s5_games.html'},
        'FFA Leaderboard' : {'name': 'Season 5 Real time FFA Leaderboard', 'link': 'rt_s5_ffa_leaderboard.html'},
        'Teamer Leaderboard' : {'name': 'Season 5 Real time Teamer Leaderboard', 'link': 'rt_s5_teamer_leaderboard.html'},
        'Duel Leaderboard' : {'name': 'Season 5 Real time Duel Leaderboard', 'link': 'rt_s5_duel_leaderboard.html'},       
    },
    'PBC' : {
        'Game History' : {'name': 'PBC Game History', 'link': 'pbc_games.html'},
        'FFA Leaderboard' : {'name': 'PBC FFA Leaderboard', 'link': 'pbc_ffa_leaderboard.html'},
        'Teamer Leaderboard' : {'name': 'PBC Teamer Leaderboard', 'link': 'pbc_teamer_leaderboard.html'},
        'Duel Leaderboard' : {'name': 'PBC Duel Leaderboard', 'link': 'pbc_duel_leaderboard.html'},
        'FFA + Duel Leaderboard' : {'name': 'PBC FFA+Duel Leaderboard', 'link': 'pbc_ffa_duel_leaderboard.html'},
        'Combined Leaderboard' : {'name': 'PBC Combined Leaderboard', 'link': 'pbc_combined_leaderboard.html'},
    }
}

pages_list = [
    {'name': 'index', 'func': get_home_page, 'title': 'Home'},
    {'name': 'rt_games', 'func': get_realtime_history_page, 'title': 'Real time Game History'},
    {'name': 'rt_ffa_leaderboard', 'func': get_rt_ffa_leaderboard_page, 'title': 'Real time FFA Leaderboard'},
    {'name': 'rt_teamer_leaderboard', 'func': get_rt_teamer_leaderboard_page, 'title': 'Real time Teamer Leaderboard'},
    {'name': 'rt_duel_leaderboard', 'func': get_rt_duel_leaderboard_page, 'title': 'Real time Duel Leaderboard'},
    {'name': 'rt_s5_games', 'func': get_realtime_s5_history_page, 'title': 'Season 5 Real time Game History'},
    {'name': 'rt_s5_ffa_leaderboard', 'func': get_rt_s5_ffa_leaderboard_page, 'title': 'Season 5 Real time FFA Leaderboard'},
    {'name': 'rt_s5_teamer_leaderboard', 'func': get_rt_s5_teamer_leaderboard_page, 'title': 'Season 5 Real time Teamer Leaderboard'},
    {'name': 'rt_s5_duel_leaderboard', 'func': get_rt_s5_duel_leaderboard_page, 'title': 'Season 5 Real time Duel Leaderboard'},
    {'name': 'pbc_games', 'func': get_pbc_history_page, 'title': 'PBC Game History'},
    {'name': 'pbc_ffa_duel_leaderboard', 'func': get_pbc_ffa_duel_leaderboard_page, 'title': 'PBC FFA+Duel Leaderboard'},
    {'name': 'pbc_combined_leaderboard', 'func': get_pbc_combined_leaderboard_page, 'title': 'PBC FFA+Duel Leaderboard'},
    {'name': 'pbc_ffa_leaderboard', 'func': get_pbc_ffa_leaderboard_page, 'title': 'PBC FFA Leaderboard'},
    {'name': 'pbc_teamer_leaderboard', 'func': get_pbc_teamer_leaderboard_page, 'title': 'PBC Teamer Leaderboard'},
    {'name': 'pbc_duel_leaderboard', 'func': get_pbc_duel_leaderboard_page, 'title': 'PBC Duel Leaderboard'},
]

for page in pages_list:
    page_name = f'{page['name']}.html'
    print(f'Creating {page_name}')
    get_page_function = page['func']
    # if page_name == 'pbc_games.html':
    docStr = get_page_function(pages_list, menu_list)
    with open(page_name, 'w') as f:
        f.write(docStr)

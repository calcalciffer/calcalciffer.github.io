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
from pages.pbc_history import *
from pages.pbc_ffa_duel_leaderboard import *
from pages.pbc_ffa_leaderboard import *
from pages.pbc_teamer_leaderboard import *
from pages.pbc_duel_leaderboard import *

pages_list = [
    {'name': 'index', 'func': get_home_page, 'title': 'Home'},
    {'name': 'rt_games', 'func': get_realtime_history_page, 'title': 'Real time Game History'},
    {'name': 'rt_ffa_leaderboard', 'func': get_rt_ffa_leaderboard_page, 'title': 'Real time FFA Leaderboard'},
    {'name': 'rt_teamer_leaderboard', 'func': get_rt_teamer_leaderboard_page, 'title': 'Real time Teamer Leaderboard'},
    {'name': 'rt_duel_leaderboard', 'func': get_rt_duel_leaderboard_page, 'title': 'Real time Duel Leaderboard'},
    {'name': 'pbc_games', 'func': get_pbc_history_page, 'title': 'PBC Game History'},
    {'name': 'pbc_ffa_duel_leaderboard', 'func': get_pbc_ffa_duel_leaderboard_page, 'title': 'PBC FFA+Duel Leaderboard'},
    {'name': 'pbc_ffa_leaderboard', 'func': get_pbc_ffa_leaderboard_page, 'title': 'PBC FFA Leaderboard'},
    {'name': 'pbc_teamer_leaderboard', 'func': get_pbc_teamer_leaderboard_page, 'title': 'PBC Teamer Leaderboard'},
    {'name': 'pbc_duel_leaderboard', 'func': get_pbc_duel_leaderboard_page, 'title': 'PBC Duel Leaderboard'},
]

for page in pages_list:
    page_name = f'{page['name']}.html'
    print(f'Creating {page_name}')
    get_page_function = page['func']
    # if page_name == 'pbc_games.html':
    docStr = get_page_function(pages_list)
    with open(page_name, 'w') as f:
        f.write(docStr)

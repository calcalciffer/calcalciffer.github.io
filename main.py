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
from pages.pbc_history import *
from pages.ffa_duel_leaderboard import *
from pages.ffa_leaderboard import *
from pages.teamer_leaderboard import *
from pages.duel_leaderboard import *

pages_list = [
    {'name': 'index', 'func': get_home_page, 'title': 'Home'},
    {'name': 'pbc_games', 'func': get_pbc_history_page, 'title': 'Game History'},
    {'name': 'ffa_duel_leaderboard', 'func': get_ffa_duel_leaderboard_page, 'title': 'FFA+Duel Leaderboard'},
    {'name': 'ffa_leaderboard', 'func': get_ffa_leaderboard_page, 'title': 'FFA Leaderboard'},
    {'name': 'teamer_leaderboard', 'func': get_teamer_leaderboard_page, 'title': 'Teamer Leaderboard'},
    {'name': 'duel_leaderboard', 'func': get_duel_leaderboard_page, 'title': 'Duel Leaderboard'},
]

for page in pages_list:
    page_name = f'{page['name']}.html'
    get_page_function = page['func']
    docStr = get_page_function(pages_list)
    with open(page_name, 'w') as f:
        f.write(docStr)

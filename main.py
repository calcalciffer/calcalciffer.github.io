from bs4 import BeautifulSoup
import sqlite3
import re
from concurrent.futures import ThreadPoolExecutor

import dominate
from dominate.tags import *

from HTMLgenerator import *

langs = ['de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'en_US', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']

def generate_leader_html_file(bbg_ver, l):
    docStr = get_leader_html_file(bbg_ver, l)
    # print(f'writing ver={bbg_ver} lang={l}')
    if bbg_ver == None:
        with open(f'{l}/leaders_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/leaders_{bbg_ver}.html', 'w') as f:
            f.write(docStr)

def generate_city_state_html_file(bbg_ver, l):
    docStr = get_city_state_html_file(bbg_ver, l)
    # print(f'writing ver={bbg_ver} lang={l}')
    if bbg_ver == None:
        with open(f'{l}/city_states_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/city_states_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
def generate_pantheon_html_file(bbg_ver, l):
    docStr = get_pantheon_html_file(bbg_ver, l)
    # print(f'writing ver={bbg_ver} lang={l}')
    if bbg_ver == None:
        with open(f'{l}/pantheons_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/pantheons_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
def generate_religion_html_file(bbg_ver, l):
    docStr = get_religion_html_file(bbg_ver, l)
    # print(f'writing ver={bbg_ver} lang={l}')
    if bbg_ver == None:
        with open(f'{l}/religion_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/religion_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
for bbg_ver in bbg_versions:
    for l in langs:
        generate_leader_html_file(bbg_ver, l)
        generate_city_state_html_file(bbg_ver, l)
        generate_pantheon_html_file(bbg_ver, l)
        generate_religion_html_file(bbg_ver, l)
generate_leader_html_file('Beta', 'en_US')
generate_city_state_html_file('Beta', 'en_US')
generate_pantheon_html_file('Beta', 'en_US')
generate_religion_html_file('Beta', 'en_US')
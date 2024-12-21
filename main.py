from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.tags import *

from HTMLgenerator import *

langs = ['de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'en_US', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']

for bbg_ver in bbg_versions:
    for l in langs:
        docStr = get_leader_html_file(bbg_ver, l)
        if bbg_ver == None:
            with open(f'{l}/leaders_base_game.html', 'w') as f:
                f.write(docStr)
        else:
            with open(f'{l}/leaders_{bbg_ver}.html', 'w') as f:
                f.write(docStr)

docStr = get_leader_html_file('Beta', 'en_US')
with open(f'en_US/leaders_Beta.html', 'w') as f:
    f.write(docStr)
    
docStr = get_city_state_html_file('Beta', 'en_US')
with open(f'en_US/city_states_Beta.html', 'w') as f:
    f.write(docStr)
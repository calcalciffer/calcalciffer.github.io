from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.tags import *

from leaderHTMLgenerator import *

langs = ['de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'en_US', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']

for bbg_ver in bbg_versions:
    for l in langs:
        docStr = get_html_file('..', bbg_ver, l)
        with open(f'{l}/leaders_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
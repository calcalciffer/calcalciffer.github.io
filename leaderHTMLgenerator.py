from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.tags import *

from parseBBGFiles import *

replacements = [
    '[ICON_AMENITIES]',
    '[ICON_ARMY]',
    '[ICON_BARBARIAN]',
    '[ICON_CAPITAL]',
    '[ICON_CHARGES]',
    '[ICON_CITIZEN]',
    '[ICON_CIVICBOOSTED]',
    '[ICON_CORPS]',
    '[ICON_CULTURE]',
    '[ICON_DISTRICT_HOLY_SITE]',
    '[ICON_DISTRICT_INDUSTRIAL_ZONE]',
    '[ICON_DISTRICT]',
    '[ICON_ENVOY]',
    '[ICON_FAITH]',
    '[ICON_FAVOR]',
    '[ICON_FOOD]',
    '[ICON_INFLUENCEPERTURN]',
    '[ICON_GLORY_DARK_AGE]',
    '[ICON_GLORY_NORMAL_AGE]',
    '[ICON_GLORY_GOLDEN_AGE]',
    '[ICON_GLORY_SUPER_GOLDEN_AGE]',
    '[ICON_GOLD]',
    '[ICON_GOVERNMENT]',
    '[ICON_GOVERNOR]',
    '[ICON_GREATADMIRAL]',
    '[ICON_GREATARTIST]',
    '[ICON_GREATENGINEER]',
    '[ICON_GREATGENERAL]',
    '[ICON_GREATMERCHANT]',
    '[ICON_GREATMUSICIAN]',
    '[ICON_GREATPERSON]',
    '[ICON_GREATPROPHET]',
    '[ICON_GREATSCIENTIST]',
    '[ICON_GREATWORK_ARTIFACT]',
    '[ICON_GREATWORK_LANDSCAPE]',
    '[ICON_GREATWORK_MUSIC]',
    '[ICON_GREATWORK_RELIC]',
    '[ICON_GREATWORK_PORTRAIT]',
    '[ICON_GREATWORK_SCULPTURE]',
    '[ICON_GREATWORK_WRITING]',
    '[ICON_GREATWORK_RELIGIOUS]',
    '[ICON_GREATWRITER]',
    '[ICON_STAT_GRIEVANCE]',
    '[ICON_HOUSING]',
    '[ICON_MOVEMENT]',
    # '[ICON_POPULATION]',
    '[ICON_POWER]',
    '[ICON_PRODUCTION]',
    '[ICON_PROMOTION]',
    '[ICON_RANGE]',
    '[ICON_RANGED]',
    '[ICON_RELIGION]',
    '[ICON_RESOURCE_COAL]',
    '[ICON_RESOURCE_IRON]',
    '[ICON_SCIENCE]',
    '[ICON_STRENGTH]',
    '[ICON_TECHBOOSTED]',
    '[ICON_TOURISM]',
    '[ICON_TRADEROUTE]',
    '[ICON_TRADINGPOST]',
    '[ICON_TURN]',
    '[ICON_VISLIMITED]'
]

civ_leaders_items = get_civs_tables("sqlFiles/DebugConfiguration.sqlite")

bbg_versions = ['5.8', '6.0', '6.1']
def add_header(curr_ver):
    with div(cls='dropdown'):
        button('BBG Version', cls='dropbtn')
        with div(cls="dropdown-content"):
            for v in bbg_versions:
                a(f'BBG {v}', href=f'leaders_{v}.html')
    with div(style="text-align:center"):
        p(f'BBG {curr_ver} Leader Descriptions')
    with div(style="text-align:right"):
        a(img(src='../assets/flags/4x3/us.svg', height='16px'), href=f'../en_US/leaders_{curr_ver}.html')
        a(img(src='../assets/flags/4x3/fr.svg', height='16px'), href=f'../fr_FR/leaders_{curr_ver}.html')
        br()
        # a(img(src='../assets/flags/4x3/ru.svg', height='16px'), href=f'../ru_RU/leaders_{curr_ver}.html')
        a(img(src='../assets/flags/4x3/cn.svg', height='16px'), href=f'../zh_Hans_CN/leaders_{curr_ver}.html')
        a(img(src='../assets/flags/4x3/kr.svg', height='16px'), href=f'../ko_KR/leaders_{curr_ver}.html')

def add_sidebar_header(relative_path):
    with span(cls="image"):
        img(src=f"{relative_path}/images/logo.png")
    with p():
        strong('Civ VI With BBG')

def add_final_scripts(relative_path):
    script(src=f"{relative_path}/assets/js/jquery.min.js")
    script(src=f"{relative_path}/assets/js/browser.min.js")
    script(src=f"{relative_path}/assets/js/breakpoints.min.js")
    script(src=f"{relative_path}/assets/js/util.js")
    script(src=f"{relative_path}/assets/js/main.js")

def get_html_file(relative_path, bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None)
    with doc.head:
        script(_async=True, src="https://www.googletagmanager.com/gtag/js?id=G-SKC1VQF10G")
        script('''
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-SKC1VQF10G');
    ''')
        title(f'BBG {bbg_version} Leader Description')
        link(rel='icon', href=f'{relative_path}/images/civVI.webp', type='image/x-icon')
        link(rel='stylesheet', href=f"{relative_path}/assets/css/main.css")
        meta(charset='utf-8')
        meta(name="viewport", content="width=device-width, initial-scale=1, user-scalable=no")
# <script async src="https://www.googletagmanager.com/gtag/js?id=G-SKC1VQF10G"></script>
# <script>
#   window.dataLayer = window.dataLayer || [];
#   function gtag(){dataLayer.push(arguments);}
#   gtag('js', new Date());

#   gtag('config', 'G-SKC1VQF10G');
# </script>


    with doc.body:
        attr(cls='is-preload')

    menu_items = []
    with doc:
        with div(id="wrapper"):
            with div(id="main"):
                with div(cls="inner"):
                    with header(id="header"):
                        add_header(bbg_version)
                    with section(id="banner"):
                        with div():
                            attr(cls="content")
                            for leader in civ_leaders_items:
                                menu_items.append(locs_data[leader[2]] + ' ' + locs_data[leader[5]])
                                with div(id=locs_data[leader[2]] + ' ' + locs_data[leader[5]]):
                                    with h2(locs_data[leader[2]] + ' ' + locs_data[leader[5]]):
                                        img(src=f'{relative_path}/images/leaders/{en_US_locs_data[leader[2]] + ' ' + en_US_locs_data[leader[5]]}.webp', style="vertical-align: middle")
                                    # h2(locs_data[leader[2]] + ' ' + locs_data[leader[5]])
                                    h3(locs_data[leader[3]])
                                    p(locs_data[leader[4]])
                                    h3(locs_data[leader[6]])
                                    p(f'{locs_data[leader[7]]}')
                                    for item in civ_leaders_items[leader]:
                                        with h3(f'{locs_data[item[4]]}'):
                                            img(src=f'{relative_path}/images/items/{en_US_locs_data[item[4]]}.webp', style="vertical-align: middle; width:50px")
                                        p(f'{locs_data[item[5]]}')
                                    hr()
            with div(id="sidebar"):
                with div():
                    attr(cls="inner")
                    add_sidebar_header(relative_path)

                    with nav(id="menu"):
                        with header():
                            attr(cls='major')
                            h2('Menu')
                        with ul():
                            for i in menu_items:
                                li(a(i, href=f'#{i}'))
        add_final_scripts(relative_path)

    docStr = str(doc)
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="{relative_path}/images/{replace[1:-1]}.webp" height=16px/>', docStr)
    if docStr.find('[ICON_') != -1:
        reg = re.compile(re.escape('[ICON_'), re.IGNORECASE)
        print(f'!!!! find missing ICON replacement in BBG {bbg_version} lang:{lang}')

    return docStr

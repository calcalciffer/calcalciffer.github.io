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
    '[ICON_DISTRICT_WONDER]',
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
    '[ICON_RESOURCE_HORSES]',
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

bbg_versions = [None, '6.1', '6.0', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2']
# bbg_versions = ['5.7']
def add_header(curr_ver):
    with div():
        if curr_ver != None:
            p(f'BBG {curr_ver} Leader Descriptions')
        else:
            p(f'Civ VI GS RF Leader Descriptions')
    with div(style="text-align:right"):
        curr_ver = curr_ver if curr_ver != None else 'base_game'
        a(img(src='/assets/flags/4x3/us.svg', height='16px'), href=f'/en_US/leaders_{curr_ver}.html')
        a(img(src='/assets/flags/4x3/fr.svg', height='16px'), href=f'/fr_FR/leaders_{curr_ver}.html')
        a(img(src='/assets/flags/4x3/ru.svg', height='16px'), href=f'/ru_RU/leaders_{curr_ver}.html')
        a(img(src='/assets/flags/4x3/de.svg', height='16px'), href=f'/de_DE/leaders_{curr_ver}.html')
        a(img(src='/assets/flags/4x3/cn.svg', height='16px'), href=f'/zh_Hans_CN/leaders_{curr_ver}.html')
        a(img(src='/assets/flags/4x3/kr.svg', height='16px'), href=f'/ko_KR/leaders_{curr_ver}.html')

def add_sidebar_header(bbg_version):
    with span(cls="image"):
        img(src=f"/images/logo.png")
    with div(cls='dropdown'):
        if bbg_version == None:
            button('Base Game', cls='dropbtn')
        else:
            button(f'BBG v{bbg_version}', cls='dropbtn')
        with div(cls="dropdown-content"):
            for v in bbg_versions:
                if v == None:
                    a(f'Base Game', href=f'leaders_base_game.html')
                else:
                    a(f'BBG {v}', href=f'leaders_{v}.html')

def add_final_scripts():
    script(src=f"/assets/js/jquery.min.js")
    script(src=f"/assets/js/browser.min.js")
    script(src=f"/assets/js/breakpoints.min.js")
    script(src=f"/assets/js/util.js")
    script(src=f"/assets/js/main.js")
    
def get_loc(locs_data, s):
    res = locs_data[s]
    if res.find('|') == -1:
        return res
    else:
        return res[:res.find('|')]
    
def get_html_lang(lang):
    if lang == 'de_DE':
        return 'de'
    if lang == 'en_US':
        return 'en'
    if lang == 'es_ES':
        return 'es'
    if lang == 'fr_FR':
        return 'fr'
    if lang == 'it_IT':
        return 'it'
    if lang == 'ja_JP':
        return 'ja'
    if lang == 'ko_KR':
        return 'ko'
    if lang == 'pl_PL':
        return 'pl'
    if lang == 'pt_BR':
        return 'pt'
    if lang == 'ru_RU':
        return 'ru'
    if lang == 'zh_Hans_CN':
        return 'zh-Hans'

def get_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    with doc.head:
        script(_async=True, src="https://www.googletagmanager.com/gtag/js?id=G-Z2ESCT7CR0")
        script('''
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-Z2ESCT7CR0');
    ''')
        if bbg_version != None:
            title(f'BBG {bbg_version} Leader Description')
        else :
            title(f'Civ VI GS RF Leaders Description')
        link(rel='icon', href=f'/images/civVI.webp', type='image/x-icon')
        link(rel='stylesheet', href=f"/assets/css/main.css")
        meta(charset='utf-8')
        meta(name="viewport", content="width=device-width, initial-scale=1, user-scalable=no")

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
                                menu_items.append(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
                                with div(id=get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                    with h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                        img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5])}.webp', style="vertical-align: middle")
                                    # h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
                                    h3(get_loc(locs_data, leader[3]))
                                    p(get_loc(locs_data, leader[4]))
                                    h3(get_loc(locs_data, leader[6]))
                                    p(f'{get_loc(locs_data, leader[7])}')
                                    for item in civ_leaders_items[leader]:
                                        with h3(f'{get_loc(locs_data, item[4])}'):
                                            img(src=f'/images/items/{get_loc(en_US_locs_data, item[4])}.webp', style="vertical-align: middle; width:50px")
                                        p(f'{get_loc(locs_data, item[5])}')
                                    hr()
            with div(id="sidebar"):
                with div():
                    attr(cls="inner")
                    add_sidebar_header(bbg_version)

                    with nav(id="menu"):
                        with header():
                            attr(cls='major')
                            h2('Menu')
                        with ul():
                            for i in menu_items:
                                li(a(i, href=f'#{i}'))
        add_final_scripts()

    docStr = str(doc)
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="/images/{replace[1:-1]}.webp" height=16px/>', docStr)
    reg = re.compile(re.escape('[ICON_BULLET]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    docStr = docStr.replace('[ICON_THEMEBONUS_ACTIVE]', '')

    return docStr

from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.svg import *
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
    '[ICON_DISTRICT]',
    '[ICON_DISTRICT_AERODROME]',
    '[ICON_DISTRICT_AQUEDUCT]',
    '[ICON_DISTRICT_CAMPUS]',
    '[ICON_DISTRICT_CANAL]',
    '[ICON_DISTRICT_CITY_CENTER]',
    '[ICON_DISTRICT_COMMERCIAL_HUB]',
    '[ICON_DISTRICT_DAM]',
    '[ICON_DISTRICT_DIPLOMATIC_QUARTER]',
    '[ICON_DISTRICT_ENCAMPMENT]',
    '[ICON_DISTRICT_ENTERTAINMENT_COMPLEX]',
    '[ICON_DISTRICT_HARBOR]',
    '[ICON_DISTRICT_GOVERNMENT]',
    '[ICON_DISTRICT_HOLYSITE]',
    '[ICON_DISTRICT_HOLY_SITE]',
    '[ICON_DISTRICT_INDUSTRIAL_ZONE]',
    '[ICON_DISTRICT_MBANZA]',
    '[ICON_DISTRICT_NEIGHBORHOOD]',
    '[ICON_DISTRICT_LAVRA]',
    '[ICON_DISTRICT_PRESERVE]',
    '[ICON_DISTRICT_SPACEPORT]',
    '[ICON_DISTRICT_THEATER]',
    '[ICON_DISTRICT_WATER_ENTERTAINMENT_COMPLEX]',
    '[ICON_DISTRICT_WONDER]',
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
def add_header(curr_ver, lang):
    with header(cls="header"):
            with div(cls="header-inner"):
                with div(cls="container"):
                    with div(cls="inner"):
                        with div(cls="row"):
                            with div(cls="col-lg-3 col-md-3 col-12"):
                                with div(cls="logo"):
                                    with a(href="/index.html"):
                                        img(src="/images/logo.png", alt="#")
                                div(cls="mobile-nav")
                            with div(cls="col-lg-6 col-md-6 col-12"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            with li():
                                                a('Leaders', href='#')
                                            with li():
                                                a('Governors', href='#')
                                            with li():
                                                a('Pantheons', href='#')
                                            with li():
                                                a('City States', href='#')
                                            # with li():
                            with div(cls="col-lg-3 col-md-3 col-12", style="align-content: center;"):
                                with a(href=f'/en_US/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/us.svg', style='height:1em')
                                with a(href=f'/fr_FR/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/fr.svg', style='height:1em')
                                with a(href=f'/ru_RU/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/ru.svg', style='height:1em')
                                with a(href=f'/de_DE/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/de.svg', style='height:1em')
                                with a(href=f'/zh_Hans_CN/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/cn.svg', style='height:1em')
                                with a(href=f'/ko_KR/leaders_{curr_ver}.html'):
                                    img(src='/assets/flags/4x3/kr.svg', style='height:1em')
    
    # with div():
    #     if curr_ver != None:
    #         p(f'BBG {curr_ver} Leader Descriptions')
    #     else:
    #         p(f'Civ VI GS RF Leader Descriptions')
    # with div(style="text-align:right"):
    # # with div(id='menu'):
    # #     button(f'Leaders', style='text-transform: none', href=f'/{lang}/leaders_{curr_ver}.html')
    # #     button(f'Governors', style='text-transform: none')
    # #     button(f'Pantheons', style='text-transform: none')
    # # with div(id='icons'):
    #     curr_ver = curr_ver if curr_ver != None else 'base_game'
    #     a(img(src='/assets/flags/4x3/us.svg', height='16px'), href=f'/en_US/leaders_{curr_ver}.html')
    #     a(img(src='/assets/flags/4x3/fr.svg', height='16px'), href=f'/fr_FR/leaders_{curr_ver}.html')
    #     a(img(src='/assets/flags/4x3/ru.svg', height='16px'), href=f'/ru_RU/leaders_{curr_ver}.html')
    #     a(img(src='/assets/flags/4x3/de.svg', height='16px'), href=f'/de_DE/leaders_{curr_ver}.html')
    #     a(img(src='/assets/flags/4x3/cn.svg', height='16px'), href=f'/zh_Hans_CN/leaders_{curr_ver}.html')
    #     a(img(src='/assets/flags/4x3/kr.svg', height='16px'), href=f'/ko_KR/leaders_{curr_ver}.html')

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
    script(src="/js/jquery.min.js")
    script(src="/js/jquery-migrate-3.0.0.js")
    script(src="/js/jquery-ui.min.js")
    script(src="/js/easing.js")
    script(src="/js/colors.js")
    script(src="/js/popper.min.js")
    script(src="/js/bootstrap-datepicker.js")
    script(src="/js/jquery.nav.js")
    script(src="/js/slicknav.min.js")
    script(src="/js/jquery.scrollUp.min.js")
    script(src="/js/niceselect.js")
    script(src="/js/tilt.jquery.min.js")
    script(src="/js/owl-carousel.js")
    script(src="/js/jquery.counterup.min.js")
    script(src="/js/steller.js")
    script(src="/js/wow.min.js")
    script(src="/js/jquery.magnific-popup.min.js")
    script(src="http://cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js")
    script(src="/js/bootstrap.min.js")
    script(src="/js/main.js")
    
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

    doc = dominate.document(title=None, lang=get_html_lang(lang), cls="no-js")
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
        link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap")
        link(rel='stylesheet', href=f"/css/bootstrap.min.css")
        link(rel='stylesheet', href=f"/css/nice-select.css")
        link(rel='stylesheet', href=f"/css/font-awesome.min.css")
        link(rel='stylesheet', href=f"/css/icofont.css")
        link(rel='stylesheet', href=f"/css/slicknav.min.css")
        link(rel='stylesheet', href=f"/css/owl-carousel.css")
        link(rel='stylesheet', href=f"/css/datepicker.css")
        link(rel='stylesheet', href=f"/css/animate.min.css")
        link(rel='stylesheet', href=f"/css/magnific-popup.css")
        link(rel='stylesheet', href=f"/css/normalize.css")
        link(rel='stylesheet', href=f"/style.css")
        link(rel='stylesheet', href=f"/css/responsive.css")
        meta(charset='utf-8')
        meta(httpequiv="X-UA-Compatible", contents="IE=edge")
        meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no")

    # doc.body

    menu_items = []
    with doc:
        with div(cls="preloader"):
            with div(cls="loader"):
                div(cls="loader-outter")
                div(cls="loader-inner")
                with div(cls="indicator"):
                    with svg(width='16px', height='12px'):
                        polyline(id="back", points="1 6 4 6 6 11 10 1 12 6 15 6")
                        polyline(id="front", points="1 6 4 6 6 11 10 1 12 6 15 6")
                        
        add_header(bbg_version, lang)

        with section(cls="Feautes section"):
            with div(cls="containter"):
                for leader in civ_leaders_items:
                    menu_items.append(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
                    with div(cls="row"):
                        with div(cls="col-lg-12"):
                            with div(cls="section-title"):
                                with div(id=get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                    with h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                        img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5])}.webp', style="vertical-align: middle")
                                    h3(get_loc(locs_data, leader[3]), style="text-align:left")
                                    p(get_loc(locs_data, leader[4]), style="text-align:left")
                                    br()
                                    h3(get_loc(locs_data, leader[6]), style="text-align:left")
                                    p(f'{get_loc(locs_data, leader[7])}', style="text-align:left")
                                    br()
                                    for item in civ_leaders_items[leader]:
                                        with h3(f'{get_loc(locs_data, item[4])}', style="text-align:left"):
                                            img(src=f'/images/items/{get_loc(en_US_locs_data, item[4])}.webp', style="vertical-align: middle; width:2em; text-align:left")
                                        p(f'{get_loc(locs_data, item[5])}', style="text-align:left")
                                        br()
                                    hr()
        #     with div(id="sidebar"):
        #         with div():
        #             attr(cls="inner")
        #             add_sidebar_header(bbg_version)

        #             with nav(id="menu"):
        #                 with header():
        #                     attr(cls='major')
        #                     h2('Menu')
        #                 with ul():
        #                     for i in menu_items:
        #                         li(a(i, href=f'#{i}'))
        add_final_scripts()

    docStr = str(doc)
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="/images/{replace[1:-1]}.webp" style="height:1.4em"/>', docStr)
    reg = re.compile(re.escape('[ICON_BULLET]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    docStr = docStr.replace('[ICON_THEMEBONUS_ACTIVE]', '')

    return docStr

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

def add_preloader():
    with div(cls="preloader"):
        with div(cls="loader"):
            div(cls="loader-outter")
            div(cls="loader-inner")
            with div(cls="indicator"):
                with svg(width="16px",height="12px"):
                    polyline(id="back", points="1 6 4 6 6 11 10 1 12 6 15 6")
                    polyline(id="front", points="1 6 4 6 6 11 10 1 12 6 15 6")

bbg_versions = [None, '6.1', '6.0', '5.8', '5.7', '5.6', '5.5', '5.4', '5.3', '5.2']
# bbg_versions = ['5.7']

def add_lang(text_name, link_name, bbg_version, flag):
    with li():
        with a(href=f"/{link_name}/leaders_{bbg_version}.html", style="align-content: center;"):
            img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")

def add_header(bbg_version, lang):
    with nav(cls="main-nav--bg"):
        with div(cls="main-nav"):
            with div(cls="header"):
                with div(cls="header-inner"):
                    with div(cls="inner"):
                        with div(cls="row"):
                            with div(cls="flex center sidebar-toggle col-xl-1 col-lg-1 col-md-1 col-1"):
                                with button(cls="transparent-btn", title="Menu", type="button"):
                                    span("Toggle menu", cls="sr-only")
                                    span(cls="icon menu-toggle", aria_hidden="true")
                            with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-2"):
                                with a(href="/index.html", style="align-content: center;"):
                                    img(src="/images/BBGLogo.png",alt="#")
                                div(cls="mobile-nav")
                            with div(cls="flex col-xl-7 col-lg-7 col-md-7 col-7"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            with li(cls="active"):
                                                a('Leaders', href="#")
                                            with li():
                                                a('City States', href="#")
                                            with li():
                                                a('Pantheons', href="#")
                                            with li():
                                                with a('BBG Version'):
                                                    i(cls="icofont-rounded-down")
                                                with ul(cls="dropdown"):
                                                    for v in bbg_versions:
                                                        with li():
                                                            if v is None:
                                                                a(f"Base Game", href=f"/{lang}/leaders_base_game.html")
                                                            else:
                                                                a(f"BBG v{v}", href=f"/{lang}/leaders_{v}.html")
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-1"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            with li():
                                                i(cls="lang-icon fa fa-language", style="font-size:50px; padding-top:7px")

                                                with ul(cls="dropdown", style="width:80px"):
                                                    add_lang('English  ', 'en_US', bbg_version, 'us')
                                                    add_lang('French  ', 'fr_FR', bbg_version, 'fr')
                                                    add_lang('Russian  ', 'ru_RU', bbg_version, 'ru')
                                                    add_lang('German  ', 'de_DE', bbg_version, 'de')
                                                    add_lang('Chinese  ', 'zh_Hans_CN', bbg_version, 'cn')
                                                    add_lang('Korean  ', 'kr_KR', bbg_version, 'kr')
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-1"):
                                with div(cls="theme-switcher-wrapper"):
                                    with button(cls="theme-switcher gray-circle-btn", type="button", title="Switch theme"):
                                        span("Switch theme", cls="sr-only")
                                        i(cls="sun-icon", data_feather="sun", aria_hidden="true")
                                        i(cls="moon-icon", data_feather="moon", aria_hidden="true")
    
def add_sidebar(menu_items):
    with aside(cls="sidebar"):
        with div(cls="sidebar-start"):
            with div(cls="sidebar-body"):
                with ul(cls="sidebar-body-menu"):
                    for item in menu_items:
                        with li():
                            with a(href=f'#{item}', onclick=f'civClicked("{item}")'):
                                with span(cls="icon", aria_hidden="true"):
                                    img(src=f'/images/leaders/{item}.webp')
                                p(item)

def add_final_scripts():
    script(src="/js/jquery.min.js")
    script(src="/js/script.js")
    script(src="/plugins/feather.min.js")
    script(src="/plugins/chart.min.js")
    script(src="https://kit.fontawesome.com/bd91c323e3.js", crossorigin="anonymous")
    
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
    
def add_html_header(doc, page_title):
    with doc.head:
        script(_async=True, src="https://www.googletagmanager.com/gtag/js?id=G-Z2ESCT7CR0")
        script('''
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-Z2ESCT7CR0');
    ''')
        title(page_title)
        link(rel='icon', href=f'/images/civVI.webp', type='image/x-icon')
        link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap")
        link(rel='stylesheet', href=f"/css/style.min.css")
        link(rel='stylesheet', href=f"/css/preloader.css")
        link(rel='stylesheet', href=f"/css/animate.min.css")
        link(rel='stylesheet', href=f"/css/header.css")
        meta(charset='utf-8')
        meta(httpequiv="X-UA-Compatible", contents="IE=edge")
        meta(name="viewport", content="width=device-width, initial-scale=1")

def get_leader_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Leader Description')
    else :
        add_html_header(doc, f'Civ VI GS RF Leaders Description')

    menu_items = []
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items)
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for leader in civ_leaders_items:
                                    with div(cls="row", id=get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]), cls='civ-name'):
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5])}.webp', style="vertical-align: middle")
                                                h3(get_loc(locs_data, leader[3]), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(get_loc(locs_data, leader[4]), style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                h3(get_loc(locs_data, leader[6]), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(f'{get_loc(locs_data, leader[7])}', style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                for item in civ_leaders_items[leader]:
                                                    with h3(f'{get_loc(locs_data, item[4])}', style="text-align:left", cls='civ-ability-name'):
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4])}.webp', style="vertical-align: middle; width:2em; text-align:left")
                                                    p(f'{get_loc(locs_data, item[5])}', style="text-align:left", cls='civ-ability-desc')
                                                    br()

        add_final_scripts()
        with a(id="scrollUp", cls="scroll-up displayNone", href="#top", style="position: fixed; z-index: 2147483647;"):
            with span():
                i(cls='fa fa-angle-up')

    docStr = str(doc)
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="/images/{replace[1:-1]}.webp" style="height:1em"/>', docStr)
    reg = re.compile(re.escape('[ICON_BULLET]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    docStr = docStr.replace('[ICON_THEMEBONUS_ACTIVE]', '')

    return docStr
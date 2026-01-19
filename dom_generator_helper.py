from bs4 import BeautifulSoup
import sqlite3
import re
import math

import dominate
from dominate.svg import *
from dominate.tags import *

image_onerror = "this.onerror=null; this.src='/images/civVI.webp';"

def add_preloader():
    with div(cls="preloader"), div(cls="loader"):
        div(cls="loader-outter")
        div(cls="loader-inner")
        with div(cls="indicator"):
            with svg(width="16px",height="12px"):
                polyline(id="back", points="1 6 4 6 6 11 10 1 12 6 15 6")
                polyline(id="front", points="1 6 4 6 6 11 10 1 12 6 15 6")

def get_version_name(bbg_version):
    return bbg_version if bbg_version != None else 'base_game'

def add_header(page_type, pages_list, menu_list):
    with nav(cls="main-nav--bg"), div(cls="main-nav"):
        with div(cls="header"), div(cls="header-inner"), div(cls="inner"):
            with div(cls="row"):
                with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-2"):
                    with a(href="/index.html", style="align-content: center;"):
                        img(src="/images/cplLogo.webp", style="width:3em; border-radius:10%", alt="#")
                    div(cls="mobile-nav")
                with div(cls="flex col-xl-8 col-lg-8 col-md-8 col-8"), div(cls="main-menu"), nav(cls="navigation"):
                    with ul(cls="nav menu"):
                        for item in menu_list:
                            menu_item = menu_list[item]
                            print(menu_item)
                            if len(menu_item) == 1:
                                page_name = item
                                link = menu_item['Home']['link']
                                with li(cls="active" if link == f"{page_type}.html" else ""):
                                    a(page_name, href=f"/{link}", onclick=f'civClicked(null)')
                            else:
                                with li():
                                    with a(item):
                                        i(cls="icofont-rounded-down")
                                    with ul(cls="dropdown bbg-version-dropdown"):
                                        for sub_item in menu_item:
                                            with li():
                                                print(menu_item[sub_item])
                                                a(sub_item, href=f"/{menu_item[sub_item]['link']}")
                                # with li(cls="menu-item-has-children"):
                                #     a(item, href="#", onclick=f'civClicked(null)')
                                #     with ul(cls="sub-menu"):
                                #         for sub_item in menu_item:
                                #             sub_menu_item = menu_item[sub_item]
                                #             page_name = sub_menu_item['name']
                                #             link = sub_menu_item['link']
                                #             with li(cls="active" if link == f"{page_type}.html" else ""):
                                #                 a(page_name, href=f"/{link}", onclick=f'civClicked(null)')
                        # for page in pages_list:
                        #     page_name = page['title']
                        #     t = page['name']
                        #     with li(cls="active" if t == page_type else ""):
                        #         a(page_name, href=f"/{t}.html", onclick=f'civClicked(null)')
                with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-1"), div(cls='flex row justify-content-around'):
                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"), div(cls="theme-switcher-wrapper"):
                        with button(cls="theme-switcher gray-circle-btn", type="button", title="Switch theme"):
                            span("Switch theme", cls="sr-only")
                            i(cls="sun-icon", data_feather="sun", aria_hidden="true")
                            i(cls="moon-icon", data_feather="moon", aria_hidden="true")
                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"), div(cls="match-switcher-wrapper"):
                        with button(cls="match-switcher gray-circle-btn", type="button", title="Switch Gametype"):
                            span("Switch Gametype", cls="sr-only")
                            i('All', cls="all-icon", aria_hidden="true")
                            i('FFA', cls="ffa-icon", aria_hidden="true")
                            i('Te', cls="teamer-icon", aria_hidden="true")
                            i('Du', cls="duel-icon", aria_hidden="true")
    # add_footer()

def add_final_scripts():
    script(src="/js/jquery.min.js")
    script(src="/js/script.js")
    script(src="/plugins/feather.min.js")
    script(src="/plugins/chart.min.js")

def get_loc(locs_data, s):
    try:
        res = locs_data[s]
        if res.find('|') == -1:
            return res
        else:
            return res[:res.find('|')]
    except KeyError:
        print(f'KeyError: {s} not found in locs_data')
        return f'Not found: {s}'

def get_html_lang(lang):
    if len(lang) == 5:
        return lang[0 : -3]
    elif lang == 'zh_Hans_CN':
        return 'zh-Hans'
    else:
        raise ValueError(f'Unknown lang: {lang}')

def add_html_header(doc, page_title):
    with doc.head:
        title(page_title)
        meta(charset='utf-8')
        meta(httpequiv="X-UA-Compatible", contents="IE=edge")
        meta(name="viewport", content="width=device-width, initial-scale=1")
        link(rel='icon', href=f'/images/cplLogo.webp', type='image/x-icon')
        link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap")
        link(rel='stylesheet', href=f"/css/style.min.css")
        link(rel='stylesheet', href=f"/css/preloader.css")
        link(rel='stylesheet', href=f"/css/animate.min.css")
        link(rel='stylesheet', href=f"/css/header.css")
        link(rel='stylesheet', href=f"/css/footer.css")
        link(rel='stylesheet', href=f"/fontawesome-free-7.0.0-web/css/all.css")

def add_footer():
    with div(cls="scroll-up footer-popup", id="footer-popup"), div(cls="footer-popup-inner"):
        with div(cls="row"):
            with div(cls="col-sm-8 col-1 footer-popup-body"):
                p("If you like this project, any donation would be extremely helpful for me in maintaining the website.", id="donateText")
            with div(cls="col-sm-2 col-6 footer-popup-donate"):
                a("Donate", href="https://ko-fi.com/calcalciffer", target="_blank", cls="btn btn-primary")
            with div(cls="col-sm-2 col-6 footer-popup-scroll-up"):
                with a(id="scrollUp", cls="displayNone", href="#top", onclick=f'civClicked(null)'):
                    i(cls='fa-solid fa-up-long')

def create_page(title, header, pages_list, menu_list, page_content_func, *args, **kwargs):
    doc = dominate.document(title=None)
    add_html_header(doc, title)

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"), div(cls="main-wrapper"):
            add_header(header, pages_list, menu_list)
            with div(cls=""):
                with div(cls="leaders-data min-w-full"), main(cls="main users chart-page"), div(cls="container"):
                    h1(title, cls='civ-name')
                    br()
                    page_content_func(*args, **kwargs)
        add_final_scripts()

    docStr = str(doc)
    return docStr
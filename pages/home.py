from dom_generator_helper import *

def generate_home_page_content():
    with div(cls="content"):
        with div(cls="container py-4"):
            h1("Welcome to the Civilization Player League leaderboards!", cls='civ-ability-name')

def get_home_page(pages_list):
    return create_page(
        title='Civilization Player League - Home',
        header='home',
        pages_list=pages_list,
        page_content_func=generate_home_page_content
    )
from dom_generator_helper import *

def generate_home_page_content():
    with div(cls="content"):
        with div(cls="container py-4"):
            h1("Welcome to the Civilization Plus League")
            p("The Civilization Plus League (CPL) is a competitive league for Civilization VI players. Join us to compete, improve your skills, and enjoy the game with a community of like-minded players.")
            h2("Getting Started")
            p("To get started, check out the 'About' section to learn more about the league, read the 'CPL Rules' to understand how the league operates, and explore the 'Seasons' to see current and upcoming competitions.")
            h2("Stay Connected")
            p("Follow us on social media and join our Discord server to stay updated on league news, events, and discussions.")

def get_home_page(pages_list):
    return create_page(
        title='Civilization Plus League - Home',
        header='home',
        pages_list=pages_list,
        page_content_func=generate_home_page_content
    )
from dom_generator_helper import *
from pages.common import *

def generate_teamer_leaderboard():
    generate_leaderboard(rtstats.teamer_ratings)

def get_rt_teamer_leaderboard_page(pages_list, menu_list):
    return create_page(
        title='Realtime Teamer Leaderboard - Civilization Player League',
        header='realtime_teamer_leaderboard',
        pages_list=pages_list,
        menu_list=menu_list,
        page_content_func=generate_teamer_leaderboard
    )

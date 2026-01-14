from dom_generator_helper import *
from pages.common import *

def generate_teamer_leaderboard():
    generate_leaderboard(rt_season5_stats.teamer_ratings)

def get_rt_s5_teamer_leaderboard_page(pages_list, menu_list):
    return create_page(
        title='Season 5 Realtime Teamer Leaderboard - Civilization Player League',
        header='realtime_s5_teamer_leaderboard',
        pages_list=pages_list,
        menu_list=menu_list,
        page_content_func=generate_teamer_leaderboard
    )

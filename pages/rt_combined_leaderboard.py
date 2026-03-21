from dom_generator_helper import *
from pages.common import *

def generate_combined_leaderboard():
    generate_leaderboard(rtstats.combined_ratings)

def get_rt_combined_leaderboard_page(pages_list, menu_list):
    return create_page(
        title='Realtime Combined Leaderboard - Civilization Player League',
        header='realtime_combined_leaderboard',
        pages_list=pages_list,
        menu_list=menu_list,
        page_content_func=generate_combined_leaderboard
    )

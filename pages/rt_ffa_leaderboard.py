from dom_generator_helper import *
from pages.common import *

def generate_ffa_leaderboard():
    generate_leaderboard(rtstats.ffa_ratings)

def get_rt_ffa_leaderboard_page(pages_list):
    return create_page(
        title='Realtime FFA Leaderboard - Civilization Player League',
        header='realtime_ffa_leaderboard',
        pages_list=pages_list,
        page_content_func=generate_ffa_leaderboard
    )

from dom_generator_helper import *
from pages.common import *

def generate_duel_leaderboard():
    generate_leaderboard(pbcstats.duel_ratings)

def get_pbc_duel_leaderboard_page(pages_list):
    return create_page(
        title='Play By Cloud Duel Leaderboard - Civilization Players League',
        header='pbc_duel_leaderboard',
        pages_list=pages_list,
        page_content_func=generate_duel_leaderboard
    )

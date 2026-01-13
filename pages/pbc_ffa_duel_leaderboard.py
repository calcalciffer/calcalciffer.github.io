from dom_generator_helper import *
from pages.common import *

def generate_ffa_duel_leaderboard():
    generate_leaderboard(pbcstats.ffa_duel_ratings)

def get_pbc_ffa_duel_leaderboard_page(pages_list):
    return create_page(
        title='Play By Cloud FFA+Duel Leaderboard - Civilization Players League',
        header='pbc_ffa_duel_leaderboard',
        pages_list=pages_list,
        page_content_func=generate_ffa_duel_leaderboard
    )

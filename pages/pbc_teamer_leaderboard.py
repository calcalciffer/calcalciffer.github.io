from dom_generator_helper import *
from pages.common import *

def generate_teamer_leaderboard():
    generate_leaderboard(pbcstats.teamer_ratings)

def get_pbc_teamer_leaderboard_page(pages_list):
    return create_page(
        title='Play By Cloud Teamer Leaderboard - Civilization Player League',
        header='pbc_teamer_leaderboard',
        pages_list=pages_list,
        page_content_func=generate_teamer_leaderboard
    )

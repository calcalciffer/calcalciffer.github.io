from dom_generator_helper import *
from stat_analyzer.process_trueskill_pbc import *

def get_player_name(player_id: str, player_id_name_map) -> str:
    if player_id in player_id_name_map:
        return player_id_name_map[player_id]
    else:
        return player_id
    
def get_civ_name(player) -> str:
    return player.leader if player.leader else "No Civ"

def generate_ffa_duel_leaderboard():
    TSProcessor = PBCTrueSkillCalculator()
    player_id_name_map = TSProcessor.build_player_id_name_map()
    _, _, _, ratings, _ = TSProcessor.get_pbc_matches_with_delta()
    for i, player in enumerate(ratings):
        if ratings[player].games >= 3:
            with div(cls="row"), div(cls="chart"):
                games = ratings[player].games
                wins = ratings[player].wins
                loses = games - wins
                rating = ratings[player].mu
                sigma = round(ratings[player].sigma, 2)
                name = get_player_name(player, player_id_name_map)
                p(f"#{i + 1} - {rating} +/- {sigma} [{wins} - {loses}] {name}", cls='civ-ability-name')

def get_pbc_ffa_duel_leaderboard_page(pages_list):
    return create_page(
        title='Play By Cloud FFA+Duel Leaderboard - Civilization Players League',
        header='pbc_ffa_duel_leaderboard',
        pages_list=pages_list,
        page_content_func=generate_ffa_duel_leaderboard
    )

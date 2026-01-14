from dom_generator_helper import *
from stat_analyzer.process_trueskill import TrueSkillCalculator

def get_player_name(player_id: str, player_id_name_map) -> str:
    if player_id in player_id_name_map:
        return player_id_name_map[player_id]
    else:
        return player_id

class CPLStats:
    def __init__(self, file_path):
        TSProcessor = TrueSkillCalculator()
        self.player_id_name_map = TSProcessor.build_player_id_name_map()
        self.ffa_ratings, self.teamer_ratings, self.duel_ratings, self.ffa_duel_ratings, self.matches_list = TSProcessor.get_matches_with_delta(file_path)

def generate_leaderboard(ratings):
    for i, player in enumerate(ratings):
        if ratings[player].games >= 3:
            with div(cls="row"), div(cls="chart"):
                games = ratings[player].games
                wins = ratings[player].wins
                loses = games - wins
                rating = ratings[player].mu
                sigma = round(ratings[player].sigma, 2)
                name = get_player_name(player, rtstats.player_id_name_map)
                p(f"#{i + 1} - {rating} +/- {sigma} [{wins} - {loses}] {name}", cls='civ-ability-name')

rtstats = CPLStats('stat_analyzer/realtimeMatches.json')
pbcstats = CPLStats('stat_analyzer/pbcMatches.json')
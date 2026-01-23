from dom_generator_helper import *
from stat_analyzer.process_trueskill import TrueSkillCalculator
from stat_analyzer.match import StatModel
import json

def get_player_name(player_id: str, player_id_name_map) -> str:
    if player_id in player_id_name_map:
        return player_id_name_map[player_id]
    else:
        return player_id

class CPLStats:
    def __init__(self, file_path):
        self.TSProcessor = TrueSkillCalculator()
        self.player_id_name_map = self.TSProcessor.build_player_id_name_map()
        self.ffa_ratings, self.teamer_ratings, self.duel_ratings, self.ffa_duel_ratings, self.combined_ratings, self.matches_list = self.TSProcessor.get_matches_with_delta(file_path)

def generate_leaderboard(ratings):
    rank = 1
    for player in ratings:
        if ratings[player].games >= 3:
            with div(cls="row"), div(cls="chart"):
                games = ratings[player].games
                wins = ratings[player].wins
                loses = games - wins
                rating = ratings[player].mu
                sigma = round(ratings[player].sigma, 2)
                name = get_player_name(player, pbcstats.player_id_name_map)
                comment(player)
                p(f"#{rank} - {rating} [{wins} - {loses}] {name}", cls='civ-ability-name')
            rank = rank + 1

rtstats = CPLStats('stat_analyzer/realtimeMatches.json')
rt_season5_stats = CPLStats('stat_analyzer/season5Games.json')
pbcstats = CPLStats('stat_analyzer/pbcMatches.json')

def dump_stats(file_path, ratings):
    res = ''
    sep = ''
    for player_id in ratings:
        res = res + sep + ratings[player_id].model_dump_json(indent=4).replace("\"id\": ", "\"_id\": ")
        sep = ',\n'
    with open(file_path, 'w') as f:
        f.write('[\n' + res + '\n]')

def dump_matches(file_path, matches):
    res = ''
    sep = ''
    for m in matches:
        res = res + sep + m.model_dump_json(indent=4)
        sep = ',\n'
    with open(file_path, 'w') as f:
        f.write('[\n' + res + '\n]')

dump_stats('rtstats_ffa.json', rtstats.ffa_ratings)
dump_stats('rtstats_teamer.json', rtstats.teamer_ratings)
dump_stats('rtstats_duel.json', rtstats.duel_ratings)

dump_matches('rt_parsed_matches.json', rtstats.TSProcessor.parsed_matches_list)

dump_stats('rt_season5_stats_ffa.json', rt_season5_stats.ffa_ratings)
dump_stats('rt_season5_stats_teamer.json', rt_season5_stats.teamer_ratings)
dump_stats('rt_season5_stats_duel.json', rt_season5_stats.duel_ratings)

dump_stats('pbcstats_ffa.json', pbcstats.ffa_ratings)
dump_stats('pbcstats_teamer.json', pbcstats.teamer_ratings)
dump_stats('pbcstats_duel.json', pbcstats.duel_ratings)
dump_stats('pbcstats_combined.json', pbcstats.combined_ratings)

dump_matches('pbc_parsed_matches.json', pbcstats.TSProcessor.parsed_matches_list)
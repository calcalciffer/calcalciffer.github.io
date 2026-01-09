import numpy as np
from stat_analyzer.match import MatchParseModel, MatchModel, PlayerModel, StatModel
from pydantic import BaseModel
import json
from collections import defaultdict
from typing import Any, Dict, List
from trueskill import TrueSkill, Rating
from datetime import datetime, UTC
import copy
import sys
sys.path.append('../')

class RealtimeTrueSkillCalculator:
    TS_MU=1250
    TS_SIGMA=150
    TS_BETA=400
    TS_TAU=10
    TS_DRAW_PROB=0
    TS_SIGMA_FREE=90
    TS_TEAMER_BOOST=1.0
    MIN_POINTS_FOR_SUBS=5

    ffa_ratings = {}
    teamer_ratings = {}
    duel_ratings = {}
    ffa_duel_ratings = {}
    matches_list = []

    def __init__(self):
        self.ffa_ratings = {}
        self.teamer_ratings = {}
        self.duel_ratings = {}
        self.ffa_duel_ratings = {}
        self.matches_list = []

    def is_sub(self, player: PlayerModel) -> bool:
        for flag in player.flags:
            if flag.lower() == "sub":
                return True
        return False

    def is_subbed_out(self, player: PlayerModel) -> bool:
        for flag in player.flags:
            if flag.lower() == "subbed":
                return True
        return False

    def make_ts_env(self) -> TrueSkill:
        return TrueSkill(
            mu=self.TS_MU,
            sigma=self.TS_SIGMA,
            beta=self.TS_BETA,
            tau=self.TS_TAU,
            draw_probability=self.TS_DRAW_PROB,
        )
        
    def reset_ratings(self, id: str):
        if id in self.ffa_ratings:
            del self.ffa_ratings[id]
        if id in self.teamer_ratings:
            del self.teamer_ratings[id]
        if id in self.duel_ratings:
            del self.duel_ratings[id]
        if id in self.ffa_duel_ratings:
            del self.ffa_duel_ratings[id]

    def get_rating(self, game_type: str, id: str, player_index: int, combine_ffa_duel: bool) -> StatModel:
        ratings = {}
        if game_type == "FFA":
            if combine_ffa_duel:
                ratings = self.ffa_duel_ratings
            else:
                ratings = self.ffa_ratings
        elif game_type == "Teamer":
            ratings = self.teamer_ratings
        elif game_type == "Duel":
            if combine_ffa_duel:
                ratings = self.ffa_duel_ratings
            else:
                ratings = self.duel_ratings
        else:
            raise ValueError(f"Unsupported game type. Use 'FFA', 'Teamer' or 'Duel'. {game_type} given.")
        if id in ratings:
            rating = copy.copy(ratings[id])
            rating.index = player_index
            return rating
        return StatModel(
            index=player_index,
            id=id,
            mu=self.TS_MU,
            sigma=self.TS_SIGMA,
            games=0,
            wins=0,
            first=0,
            subbedIn=0,
            subbedOut=0,
            civs={},
            lastModified=None
        )
        
    def create_stat_model(self, player_id, player_stats_db: Dict[str, Any]) -> StatModel:
        return StatModel(
            index=0,
            id=player_id,
            mu=player_stats_db.get("mu", self.TS_MU),
            sigma=player_stats_db.get("sigma", self.TS_SIGMA),
            games=player_stats_db.get("games", 0),
            wins=player_stats_db.get("wins", 0),
            first=player_stats_db.get("first", 0),
            subbedIn=player_stats_db.get("subbedIn", 0),
            subbedOut=player_stats_db.get("subbedOut", 0),
            civs=player_stats_db.get("civs", {}),
            lastModified=player_stats_db.get("lastModified", None)
        )

    def read_json_file(self, file_path: str) -> MatchParseModel:
        with open(file_path, 'r') as file:
            return json.load(file)
        
    def update_player_stats(self, match: MatchModel, players_ranking: List[StatModel], delta_value_name: str):
        teams = defaultdict(list)
        for i, p in enumerate(match.players):
            teams[p.team].append((i, p))
        team_states: List[List[StatModel]] = [
            [players_ranking[p_index_tuple[0]] for p_index_tuple in teams[team]] for team in teams
        ]
        ts_teams = [[Rating(p.mu, p.sigma) for p in team] for team in team_states]
        placements = [teams[team][0][1].position for team in teams]
        if len(placements) <= 1:
            return None, None

        ts_env = self.make_ts_env()
        new_ts = ts_env.rate(ts_teams, ranks=placements)
        
        post: List[StatModel] = list(range(len(match.players)))
        for team_idx, team in enumerate(team_states):
            for player_index, player in enumerate(team):
                r = new_ts[team_idx][player_index]
                post[player.index] = StatModel(
                    index=player.index,
                    id=player.id,
                    mu=float(r.mu),
                    sigma=float(r.sigma),
                    games=player.games,
                    wins=player.wins,
                    first=player.first,
                    subbedIn=player.subbedIn,
                    subbedOut=player.subbedOut,
                    civs=player.civs,
                )
        for i, p in enumerate(match.players):
            p_current_ranking = players_ranking[i]
            delta = round(post[i].mu - p_current_ranking.mu) if p.id != None else 0
            if self.is_sub(p):
                # Subbed in player
                p.__setattr__(delta_value_name, max(self.MIN_POINTS_FOR_SUBS, delta))
            elif self.is_subbed_out(p):
                # Subbed out Player
                p.__setattr__(delta_value_name, delta if delta < 0 else 0)
            else:
                # Regular player
                p.__setattr__(delta_value_name, delta)
            post[i].mu = p_current_ranking.mu + getattr(p, delta_value_name)
        return match, post

    def get_player_stats_db(self, match, player, player_new_stats: StatModel, delta_value_name: str) -> Dict[str, Any]:
        player_stats_db = {}
        player_stats_db[f"mu"] = player_new_stats.mu
        player_stats_db[f"sigma"] = player_new_stats.sigma
        player_stats_db[f"games"] = player_new_stats.games + 1
        player_stats_db[f"wins"] = player_new_stats.wins + (1 if getattr(player, delta_value_name) > 0 else 0)
        player_stats_db[f"first"] = player_new_stats.first + (1 if player.position == 1 else 0)
        player_stats_db[f"subbedIn"] = player_new_stats.subbedIn + (1 if self.is_sub(player) else 0)
        player_stats_db[f"subbedOut"] = player_new_stats.subbedOut + (1 if self.is_subbed_out(player) else 0)
        player_stats_db[f"lastModified"] = datetime.now(UTC)
        if player.leader:
            civs = player_new_stats.civs
            player_civ_leader = player.leader
            civs[player_civ_leader] = civs.get(player_civ_leader, 0) + 1
            player_stats_db[f"civs"] = civs
        return player_stats_db
        
    def process_ts(self, match_parse_model: MatchParseModel):
        for match in match_parse_model.matches:
            player_ratings = [self.get_rating(match.gametype, p.id['$numberLong'], i, False) for i, p in enumerate(match.players)]
            match, post = self.update_player_stats(match, player_ratings, "delta")
            if match is None:
                continue
            self.matches_list.append((match, post))
            for i, player in enumerate(match.players):
                player_stats_db = self.get_player_stats_db(match, player, post[i], "delta")
                if match.gametype == "FFA":
                    self.ffa_ratings[player.id['$numberLong']] = self.create_stat_model(player.id['$numberLong'], player_stats_db)
                elif match.gametype == "Teamer":
                    self.teamer_ratings[player.id['$numberLong']] = self.create_stat_model(player.id['$numberLong'], player_stats_db)
                elif match.gametype == "Duel":
                    self.duel_ratings[player.id['$numberLong']] = self.create_stat_model(player.id['$numberLong'], player_stats_db)
                else:
                    raise ValueError(f"Unsupported game type. Use 'FFA', 'Teamer' or 'Duel'. {match.gametype} given.")

            if match.gametype == "FFA" or match.gametype == "Duel":
                player_ratings = [self.get_rating(match.gametype, p.id['$numberLong'], i, True) for i, p in enumerate(match.players)]
                match, post = self.update_player_stats(match, player_ratings, "delta")
                for i, player in enumerate(match.players):
                    player_stats_db = self.get_player_stats_db(match, player, post[i], "delta")
                    self.ffa_duel_ratings[player.id['$numberLong']] = self.create_stat_model(player.id['$numberLong'], player_stats_db)

    def get_realtime_matches_with_delta(self):
        file_path = 'stat_analyzer/realtimeMatches.json'
        data = self.read_json_file(file_path)
        match_parse_model = MatchParseModel(**data)
        for m in match_parse_model.matches:
            positions = set()
            for p in m.players:
                positions.add(p.position)
            if m.gametype == 'FFA':
                if len(positions) == 2:
                    m.gametype = 'Teamer'
                    if len(m.players) == 2:
                        # 1v1 FFA is actually Duel
                        m.gametype = 'Duel'
            # else:
            #     if len(positions) == 1:
            #         for p in np.arange(int(len(m.players) / 2), len(m.players)):
            #             m.players[p].position += 1
            #             m.players[p].team += 1
                    # print(m)
                    # raise ValueError(f"Teamer match with all players on the same team found. Validation Msg ID: {m.validation_msg_id}")

        self.process_ts(match_parse_model)
        
        reset_stats_ids = []
        with open('stat_analyzer/reset_realtime_stats_ids.txt', 'r') as file:
            for line in file:
                reset_stats_ids.append(line.strip())
        for id in reset_stats_ids:
            self.reset_ratings(id)

        sorted_ffa_ratings = dict(sorted(self.ffa_ratings.items(), key=lambda x: x[1].mu, reverse=True))
        sorted_teamer_ratings = dict(sorted(self.teamer_ratings.items(), key=lambda x: x[1].mu, reverse=True))
        sorted_duel_ratings = dict(sorted(self.duel_ratings.items(), key=lambda x: x[1].mu, reverse=True))
        sorted_ffa_duel_ratings = dict(sorted(self.ffa_duel_ratings.items(), key=lambda x: x[1].mu, reverse=True))
        return sorted_ffa_ratings, sorted_teamer_ratings, sorted_duel_ratings, sorted_ffa_duel_ratings, self.matches_list

    def build_player_id_name_map(self) -> Dict[str, str]:
        file_path = 'stat_analyzer/players.players.json'
        with open(file_path, 'r') as file:
            players = json.load(file)
        res = {}
        for player in players:
            res[player['discord_id']] = player['user_name']
        return res

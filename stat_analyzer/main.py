from match import MatchParseModel, MatchModel, PlayerModel, StatModel
import json

def get_pbc_matches(data) -> MatchParseModel:
    res = []
    for i, m in enumerate(data):
        match = MatchModel(**m)
        if match.gametype == 'PBC' or match.gametype == 'PBC-Teamer':
            if len(match.players) == 2:
                match.gametype = 'PBC-Duel'
            for p in match.players:
                p.team = p.position
            res.append(match)
    return res

def get_realtime_matches(data) -> MatchParseModel:
    res = []
    for i, m in enumerate(data):
        match = MatchModel(**m)
        if match.gametype == 'FFA' or match.gametype == 'Teamer' or match.gametype == 'Duel':
            if len(match.players) == 2:
                match.gametype = 'Duel'
            for p in match.players:
                p.team = p.position
            res.append(match)
        elif match.gametype == 'PBC' or match.gametype == 'PBC-Teamer' or match.gametype == 'PBC-Duel':
            pass
        else:
            raise ValueError(f"Unsupported game type. Use 'FFA', 'Teamer', 'Duel', 'PBC', 'PBC-Teamer' or 'PBC-Duel'. {match.gametype} given.")
    return res

def read_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    file_path = 'CPL_DB_BACKUP_01-26/matchs.validated.json'  # Example file path
    data = read_json_file(file_path)
    match_parse_model = MatchParseModel(matches=get_realtime_matches(data))
    print(match_parse_model.model_dump_json(indent=2))
    
    # process_ts(match_parse_model)
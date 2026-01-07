from match import MatchParseModel, MatchModel, PlayerModel, StatModel, CivCount
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

def read_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    file_path = '../CPL_DB_BACKUP_01-26/matchs.validated.json'  # Example file path
    data = read_json_file(file_path)
    match_parse_model = MatchParseModel(matches=get_pbc_matches(data))
    print(match_parse_model.model_dump_json(indent=2))
    
    # process_ts(match_parse_model)
from match import *
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

def normalize(gametype):
    if gametype == 'FFA' or gametype == 'PBC':
        return 'ffa'
    elif gametype == 'Teamer' or gametype == 'PBC-Teamer':
        return 'teamer'
    elif gametype == 'Duel' or gametype == 'PBC-Duel':
        return 'duel'
    else:
        raise ValueError('not a valid gametype')

def get_parsed_model(match: MatchModel) -> ParsedMatchModel:
    parsed_players = []
    for p in match.players:
        parsed_player = ParsedPlayerModel(
            steam_id=None,
            user_name=None,
            civ=p.leader if p.leader else "Unknown",
            team=p.team if p.team is not None else 0,
            placement=p.position if p.position is not None else 0,
            leader=p.leader,
            discord_id=p.id['$numberLong'],
            delta=p.delta if p.delta is not None else 0.0
        )
        parsed_players.append(parsed_player)
    
    parsed_match = ParsedMatchModel(
        game='civ6',  # Assuming civ6 for this example
        turn=0,  # Placeholder value
        map_type='Unknown',  # Placeholder value
        game_mode=normalize(match.gametype),
        is_cloud=True,
        players=parsed_players,
        parser_version='1.0',
        discord_messages_id_list=[],
        save_file_hash='',
        reporter_discord_id='system'
    )
    return parsed_match

def get_matches(data) -> MatchParseModel:
    res = []
    for m in data['matches']:
        match = MatchModel(**m)
        parsed_match = get_parsed_model(match)
        res.append(parsed_match)
    return res

def read_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    file_path = 'pbcMatches.json'  # Example file path
    data = read_json_file(file_path)
    match_parse_model = ParsedMatchParseModel(matches=get_matches(data))
    print(match_parse_model.model_dump_json(indent=2))
    
    # process_ts(match_parse_model)
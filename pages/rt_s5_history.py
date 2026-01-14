from dom_generator_helper import *
from pages.common import *

def get_player_name(player_id: str, player_id_name_map) -> str:
    if player_id in player_id_name_map:
        return player_id_name_map[player_id]
    else:
        return player_id

def get_civ_name(player) -> str:
    return player.leader if player.leader else "No Civ"

def generate_realtime_history_content():
    for match in reversed(rt_season5_stats.matches_list):
        with div(cls=f"row {match[0].gametype}"), div(cls="chart"):
            p(f"Gametype: {match[0].gametype}", cls='civ-ability-name')
            for player in match[0].players:
                flags = ' ' + ' '.join(player.flags)
                p(f"[ {'+' if player.delta > 0 else ''} {round(player.delta, 2)} ] {get_player_name(player.id['$numberLong'], rt_season5_stats.player_id_name_map)} {get_civ_name(player)}{flags}",
                  style="text-align:left",
                  cls='civ-ability-desc')

def get_realtime_s5_history_page(pages_list):
    return create_page(
        title='Season 5 Realtime Game History - Civilization Player League',
        header='realtime_s5_games',
        pages_list=pages_list,
        page_content_func=generate_realtime_history_content
    )

from dom_generator_helper import *
from pages.common import pbcstats

def get_player_name(player_id: str, player_id_name_map) -> str:
    if player_id in player_id_name_map:
        return player_id_name_map[player_id]
    else:
        return player_id
    
def get_civ_name(player) -> str:
    return player.leader if player.leader else "No Civ"

def generate_pbc_history_content():
    for match in reversed(pbcstats.matches_list):
        with div(cls=f"row {match[0].gametype}"), div(cls="chart"):
            p(f"Gametype: {match[0].gametype}", cls='civ-ability-name')
            for player in match[0].players:
                # print(player.id, player.delta)
                flags = ' ' + ' '.join(player.flags)
                p(f"[ {'+' if player.delta > 0 else ''} {round(player.delta, 2)} ] {get_player_name(player.id['$numberLong'], pbcstats.player_id_name_map)} {get_civ_name(player)}{flags}",
                  style="text-align:left",
                  cls='civ-ability-desc')

def get_pbc_history_page(pages_list):
    return create_page(
        title='Play By Cloud Game History - Civilization Player League',
        header='pbc_games',
        pages_list=pages_list,
        page_content_func=generate_pbc_history_content
    )

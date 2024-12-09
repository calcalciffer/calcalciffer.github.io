from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.tags import *

def get_locs_data(db_path, bbg_version, lang):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(f'SELECT * FROM LocalizedText_{lang}')
    rows = crsr.fetchall()
    
    locs = dict()
    for r in rows:
        locs[r[1]] = r[2]
        
    with open(f'bbg_xml/{bbg_version}/{lang}.xml', 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all('Replace')
    for x in b_unique:
        # print(x)
        if len(x.Text.contents) > 0:
            locs[x['Tag']] = x.Text.contents[0]
    
    return locs

def get_civs_tables(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT CivilizationType, LeaderType, CivilizationName, CivilizationAbilityName, CivilizationAbilityDescription, LeaderName, LeaderAbilityName, LeaderAbilityDescription FROM Players WHERE Domain IN ('Players:Expansion1_Players', 'Players:Expansion2_Players', 'Players:StandardPlayers')")
    rows = crsr.fetchall()
    
    rows = sorted(rows)
    civLeaders = []
    civLeaderItems = dict()
    uniques = []

    for val in rows:
        if val[0] + val[1] not in uniques:
            civLeaders.append(val)
            uniques.append(val[0] + val[1])
    
    for row in civLeaders:
        crsr.execute(f"SELECT * FROM PlayerItems WHERE CivilizationType = '{row[0]}' AND LeaderType = '{row[1]}'")
        items = crsr.fetchall()
        unique_items = []
        unique_items_names = []
        for val in items:
            if val[3] not in unique_items_names:
                unique_items.append(val)
                unique_items_names.append(val[3])
        civLeaderItems[row] = unique_items
    
    connection.close()
    return civLeaderItems
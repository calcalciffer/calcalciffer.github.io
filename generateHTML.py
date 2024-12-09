from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.tags import *


def get_locs_data(db_path, bbg_xml):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM LocalizedText_en_US")
    rows = crsr.fetchall()
    
    locs = dict()
    for r in rows:
        locs[r[1]] = r[2]
        
    with open(bbg_xml, 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all('Replace')
    for x in b_unique:
        # print(x['Tag'], x.Text.contents[0])
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

civ_leaders_items = get_civs_tables("sqlFiles/DebugConfiguration.sqlite")

locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", "bbg_xml/BBG6.1_en_US.xml")

doc = dominate.document(title='BBG 6.1 Static')

# with doc.head:
#     link(rel='stylesheet', href='style.css')
#     script(type='text/javascript', src='script.js')

with doc:
    # with div(id='header').add(ol()):
    #     for i in ['home', 'about', 'contact']:
    #         li(a(i.title(), href='/%s.html' % i))

    with div():
        attr(cls='body')
        for leader in civ_leaders_items:
            h1(locs_data[leader[2]] + ' ' + locs_data[leader[5]])
            h3(locs_data[leader[3]])
            p(locs_data[leader[4]])
            h3(locs_data[leader[6]])
            p(f'{locs_data[leader[7]]}')
            for item in civ_leaders_items[leader]:
                h3(f'{locs_data[item[4]]}')
                p(f'{locs_data[item[5]]}')
                # print('')

docStr = str(doc)
docStr = docStr.replace('[NEWLINE]', '<br>')
replacements = [
    '[ICON_AMENITIES]',
    '[ICON_ARMY]',
    '[ICON_BARBARIAN]'
    '[ICON_CAPITAL]',
    '[ICON_CHARGES]',
    '[ICON_CITIZEN]',
    '[ICON_CIVICBOOSTED]',
    '[ICON_CORPS]',
    '[ICON_CULTURE]',
    '[ICON_DISTRICT_HOLY_SITE]',
    '[ICON_DISTRICT_INDUSTRIAL_ZONE]',
    '[ICON_DISTRICT]',
    '[ICON_ENVOY]',
    '[ICON_FAITH]',
    '[ICON_FAVOR]',
    '[ICON_FOOD]',
    '[ICON_GLORY_GOLDEN_AGE]',
    '[ICON_GLORY_NORMAL_AGE]',
    '[ICON_GLORY_SUPER_GOLDEN_AGE]',
    '[ICON_GOLD]',
    '[ICON_GOVERNMENT]',
    '[ICON_GOVERNOR]',
    '[ICON_GREATADMIRAL]',
    '[ICON_GREATARTIST]',
    '[ICON_GREATENGINEER]',
    '[ICON_GREATGENERAL]',
    '[ICON_GREATMERCHANT]',
    '[ICON_GREATMUSICIAN]',
    '[ICON_GREATPERSON]',
    '[ICON_GREATPROPHET]',
    '[ICON_GREATSCIENTIST]',
    '[ICON_GREATWORK_ARTIFACT]',
    '[ICON_GREATWORK_LANDSCAPE]',
    '[ICON_GREATWORK_MUSIC]',
    '[ICON_GREATWORK_RELIC]',
    '[ICON_GREATWORK_SCULPTURE]',
    '[ICON_GREATWORK_WRITING]',
    '[ICON_GREATWRITER]',
    '[ICON_HOUSING]',
    '[ICON_MOVEMENT]',
    '[ICON_POWER]',
    '[ICON_PRODUCTION]',
    '[ICON_PROMOTION]',
    '[ICON_RANGE]',
    '[ICON_RANGED]',
    '[ICON_RELIGION]',
    '[ICON_RESOURCE_COAL]',
    '[ICON_RESOURCE_IRON]',
    '[ICON_SCIENCE]',
    '[ICON_STRENGTH]',
    '[ICON_TECHBOOSTED]',
    '[ICON_TOURISM]',
    '[ICON_TRADEROUTE]',
    '[ICON_TRADINGPOST]',
    '[ICON_TURN]',
    '[ICON_VISLIMITED]'
]

for replace in replacements:
    reg = re.compile(re.escape(replace), re.IGNORECASE)
    docStr = reg.sub(f'<img src="./images/{replace[1:-1]}.webp" height=16px/>', docStr)

with open('index.html', 'w') as f:
    f.write(docStr)
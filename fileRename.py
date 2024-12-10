import os
import sys

if len(sys.argv) < 2:
    print('folder path not given!!')
    exit(-1)
folder_path = sys.argv[1]

lang_dict = {
    'chinese': 'zh_Hans_CN',
    'english': 'en_US',
    'french': 'fr_FR',
    'german': 'de_DE',
    'italian': 'it_IT',
    'japanese': 'ja_JP',
    'korean': 'ko_KR',
    'polish': 'pl_PL',
    'portuguese': 'pt_BR',
    'russian': 'ru_RU',
    'spanish': 'es_ES',
}

for l in lang_dict:
    print(l)
    os.rename(f'{folder_path}/{l}.xml', f'{folder_path}/{lang_dict[l]}.xml')
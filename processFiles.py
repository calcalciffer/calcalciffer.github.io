import sys
import os

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.readlines()

    data[12] = f'		<meta http-equiv="refresh" content="5; URL=https://civ6bbg.github.io/{filename}" />\n'

    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(data)
        
languages = [
    'de_DE',
    'en_US',
    'es_ES',
    'fr_FR',
    'it_IT',
    'ja_JP',
    'ko_KR',
    'pl_PL',
    'pt_BR',
    'ru_RU',
    'zh_Hans_CN'
]
for lang in languages:
    for file in os.listdir(f'{lang}/'):
        filename = f'{lang}/{file}'
        process_file(filename)
        print(f'Processed {filename}')
from pprint import pprint

import requests

melbet_tennis_api = requests.get('http://0.0.0.0:8085/api/favorit/soccer').json()
favorit_tennis_api = requests.get('http://0.0.0.0:8085/api/melbet/soccer').json()


full_lst1 = []
full_lst2 = []

api = {}

from app.fork_finder.main import find_fork


def generate_api(melbet_game, favorit_game):
    try:
        api["coefficients"] = {"1": melbet_game['events']['1'], "2": favorit_game['events']['2']}
        print(find_fork(api))
        print(melbet_game['name'], '|||', favorit_game['name'])
        print(melbet_game['url'], '@', favorit_game['url'])

    except Exception:
        pass

    try:
        api["coefficients"] = {"2": melbet_game['events']['2'], "1": favorit_game['events']['1']}
        print(find_fork(api))
        print(melbet_game['name'], '|||', favorit_game['name'])
        print(melbet_game['url'], '@', favorit_game['url'])

    except:
            pass

count = 0
for q in melbet_tennis_api['games']:
    for f in favorit_tennis_api['games']:
        if len(set(f['name'].replace('-', '').lower().split()).intersection(
                set(q['name'].replace('/', '').replace('-', '').replace('.', '').lower().split()))) >= 3:
            generate_api(q, f)
            count += 1

print(count)
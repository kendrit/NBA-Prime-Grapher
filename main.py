from nba_api.stats.static import players
from collections import Counter
import requests
import time
import pandas
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://stats.nba.com/'
}

# Only available after v1.1.0
# Proxy Support, Custom Headers Support, Timeout Support (in seconds)

def getPrime(input_name):
    player = players.find_players_by_full_name(input_name)[0]
    # {'id': 2544, 'full_name': 'LeBron James', 'first_name': 'LeBron', 'last_name': 'James', 'is_active': True}

    pid = player['id']
    pname = player['full_name']
    print(f"Selected Player ID: {pid}")

    player_info = commonplayerinfo.CommonPlayerInfo(player_id=pid, headers=custom_headers, timeout=100)

    # player_games = cumestatsplayergames.CumeStatsPlayerGames(player_id=pid)

    # games = player_games.get_dict()

    # game_ids = []

    # for i in games['resultSets'][0]['rowSet']:
    #     game_ids.append(i[1])

    player_stats = playercareerstats.PlayerCareerStats(player_id=pid)

    player_stats = player_stats.get_normalized_dict()

    player_regszn_stats = player_stats['SeasonTotalsRegularSeason']

    max_dict = {
        "pts": [0, ""],
        "ast": [0, ""],
        "stl": [0, ""],
        "blk": [0, ""],
        "reb": [0, ""],
        "ft_pct": [0, ""],
        "fg3_pct": [0, ""],
        "fg_pct": [0, ""]
    }

    max_dict = {}

    keys = ['GP', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'PTS']

    for key in keys:
        max_dict[key] = [0, ""]

    for i in player_regszn_stats:
        for key in keys[1:]:
            if key[-3:] != 'PCT' and key != 'GP':
                if (i[key] / i["GP"]) > max_dict[key][0] and i["GP"] > 41:
                    max_dict[key][0] = i[key] / i["GP"]
                    max_dict[key][1] = i["SEASON_ID"]
            else:
                if (i[key]) > max_dict[key][0] and i["GP"] > 41:
                    max_dict[key][0] = i[key]
                    max_dict[key][1] = i["SEASON_ID"]
    best_seasons = []
    for key in keys:
        best_seasons.append(max_dict[key][1])
    print(max_dict)
    return Counter(best_seasons).most_common(1)
    # for i in player_stats.get_data_frames()[0]:
    #     i.to_csv(f'{pid} {time.time()}.csv')

    # for ind, i in enumerate(player_info.get_data_frames()):
    #     i.to_csv(f'{pname} {ind}.csv')

while True:
    input_name = input("Enter a player name, or q to quit: ")
    if input_name == 'q':
        break
    print(f"{input_name}'s prime year was {getPrime(input_name)}")

print("Finished")
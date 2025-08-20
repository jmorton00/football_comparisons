import os
from dotenv import load_dotenv, find_dotenv
import json
import pandas as pd
import requests

load_dotenv(find_dotenv())

HOST = os.environ.get("X_RAPIDAPI_HOST")
KEY = os.environ.get("X_RAPIDAPI_KEY")

base_url = HOST
headers = {
    'x-rapidapi-key': KEY
    }

def call_api(endpoint, params):
    url = base_url + endpoint
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def team_info():
    teams = call_api("/teams", {"league": 39, "season": 2023})

    team_info_extracted = extract_teams(teams)

    for t in team_info_extracted:
        print(f"{t['id']}: {t['name']} ({t['country']}) - {t['venue']}")

def extract_teams(data):
    teams = []
    for item in data.get("response", []):
        team = item.get("team", {})
        venue = item.get("venue", {})
        teams.append({
            "id": team.get("id"),
            "name": team.get("name"),
            "country": team.get("country"),
            "venue": venue.get("name"),
        })
    return teams

def all_player_info(page, total_players):
    players = call_api("/players", {"league": 39, "season": 2023, "page": page})
    total_players.append(players)

    # doesn't work in free version, page max is 3
    # if players['paging']['current'] < players['paging']['total']:
    #     player_info(page+1)

    if int(players['paging']['current']) < 3:
        all_player_info(page+1, total_players)
    
    return total_players

def extract_players(data):

    players_list = []

    for page_data in data:
        for item in page_data.get("response", []):
            player = item.get("player", {})
            stats = item.get("statistics", [{}])[0]  # take first stats object
            team = stats.get("team", {})
            league = stats.get("league", {})
            games = stats.get("games", {})

            players_list.append({
                "id": player.get("id"),
                "name": player.get("name"),
                "firstname": player.get("firstname"),
                "lastname": player.get("lastname"),
                "age": player.get("age"),
                "birth_date": player.get("birth", {}).get("date"),
                "birth_place": player.get("birth", {}).get("place"),
                "birth_country": player.get("birth", {}).get("country"),
                "nationality": player.get("nationality"),
                "height": player.get("height"),
                "weight": player.get("weight"),
                "injured": player.get("injured"),
                "photo": player.get("photo"),
                "team_id": team.get("id"),
                "team_name": team.get("name"),
                "league_id": league.get("id"),
                "league_name": league.get("name"),
                "league_country": league.get("country"),
                "season": league.get("season"),
                "position": games.get("position")
            })

    return players_list

def call_all_player_info():
    total_players = all_player_info(1, [])
    extracted_total_players = extract_players(total_players)
    print(len(extracted_total_players))
    for p in extracted_total_players:
        print(f"{p['name']} ({p['nationality']}) - {p['team_name']} - {p['position']}")

def player_info(season, player_id):
    player = call_api("/players", {"season": season, "id": player_id})
    return player

def squads(team):
    squad = call_api("/players/squads", {"team":team})
    return squad

print(squads(34))
print(player_info(2023, 723))
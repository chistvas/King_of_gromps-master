import mwclient
import json
import time
from riotwatcher import LolWatcher
from application import app, db
from application.models import Summoner, Game, Proplayers, Summoner_ru, Game_ru

KEY = "RGAPI-49d594ce-ec25-4351-8ed3-764a452d17e1"
KDA = ["kills", "deaths", "assists"]
TABLE_STATS = ["championName", "win"]
PRO_PLAYER_LIST = []

def two_players_search(player1_nickname, player2_nickname, region_name, count=20):
    watcher = LolWatcher(KEY)
    player1 = watcher.summoner.by_name(region_name, player1_nickname)
    player2 = watcher.summoner.by_name(region_name, player2_nickname)
    match_list = watcher.match.matchlist_by_puuid(region_name, player1["puuid"], count=count)
    games_together = []
    for match in match_list:
        match_info = watcher.match.by_id(region_name, match)
        for player in match_info["metadata"]["participants"]:
            if player == player2["puuid"]:
                games_together.append({match: player})
        time.sleep(0.1)
    return games_together


def pro_player_search(player_nickname, region_name, count=20):
    watcher = LolWatcher(KEY)
    summoner_in_db = Summoner.query.filter_by(nickname=player_nickname).first()
    if summoner_in_db is None:
        player1 = watcher.summoner.by_name(region_name, player_nickname)
        match_list = watcher.match.matchlist_by_puuid(region_name, player1["puuid"], count=count)
    else:
        player1 = summoner_in_db.puuid
        match_list = watcher.match.matchlist_by_puuid(region_name, player1, count=count)
    games_together = []
    for match in match_list:
        match_info = watcher.match.by_id(region_name, match)
        for player in match_info["metadata"]["participants"]:
            for pro_player in pro_player_list:
                if player == pro_player:
                    games_together.append({match: player})
        time.sleep(0.1)
    return games_together


def get_match_info(match_id, region_name):
    watcher = LolWatcher(KEY)
    match_info = watcher.match.by_id(region_name, match_id)
    return match_info


def get_player_all_stats(match_id, region_name, player_puuid):
    watcher = LolWatcher(KEY)
    match_info = watcher.match.by_id(region_name, match_id)
    for i in range(10):
        if match_info["info"]["participants"][i]["puuid"] == player_puuid:
            player_info = match_info["info"]["participants"][i]
            return [player_info, match_info]


def get_player_list_stats(player_stats, list_stats):
    stats = {}
    for stat in list_stats:
        stats[stat] = player_stats[stat]
    return stats


def get_players_kda_from_scratch(player_name, region_name, match_id):
    watcher = LolWatcher(KEY)
    KDA = ["kills", "deaths", "assists"]
    player_puuid = watcher.summoner.by_name(region_name, player_name)
    player_stats = get_player_all_stats(match_id, region_name, player_puuid)
    return get_player_list_stats(player_stats, KDA)


def get_all_players_list_stats(region_name, match_id, list_stats):
    watcher = LolWatcher(KEY)
    all_player_stats = {}
    match_info = watcher.match.by_id(region_name, match_id)
    for i in range(10):
        player_info = match_info["info"]["participants"][i]
        stats = get_player_list_stats(player_info, list_stats)
        all_player_stats[watcher.summoner.by_puuid(region_name, match_info["info"]["participants"][i]["puuid"])["name"]] = stats
    return all_player_stats


def collapsed_table_info(player, region, match_id):
    watcher = LolWatcher(KEY)
    player_puuid = watcher.summoner.by_name(region, player)["puuid"]
    player1_stats, gamedata = get_player_all_stats(match_id, region, player_puuid)
    info = get_player_list_stats(player1_stats, TABLE_STATS)
    if info["win"]:
        info["win"] = "Victory"
    else:
        info["win"] = "Defeat"
    info["kda"] = ", ".join([
        str(player1_stats["kills"]),
        str(player1_stats["deaths"]),
        str(player1_stats["assists"])
        ])
    info["items"] = [
        player1_stats["item0"],
        player1_stats["item1"],
        player1_stats["item2"],
        player1_stats["item3"],
        player1_stats["item4"],
        player1_stats["item5"]
        ]
    info["items"][:] = (item for item in info["items"] if item != 0)
    left_side_prt = {}
    right_side_prt = {}
    i=0
    for participant in gamedata["metadata"]["participants"]:
        summoner_in_db = Summoner.query.filter_by(puuid=participant).first()
        if summoner_in_db is not None:
            name = summoner_in_db.nickname
            if i <= 4:
                left_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
            else:
                right_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
        else:
            name = watcher.summoner.by_puuid(region, participant)["name"]
            new_summoner = Summoner(puuid=participant, nickname=name)
            db.session.add(new_summoner)
            game_in_db = Game.query.filter_by(game_id=match_id).first()
            if game_in_db is not None:
                new_summoner.games.append(game_in_db)
            else:
                new_summoner.games.append(Game(game_id=match_id))
            db.session.commit()
            if i <= 4:
                left_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
            else:
                right_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
        time.sleep(0.1)
        i += 1
    info["left_side_prt"] = left_side_prt
    info["right_side_prt"] = right_side_prt
    return info


def crawling_data(region):
    watcher = LolWatcher(KEY)
    i=1
    summoner = Summoner.query.filter_by(id=i).first()
    puuid = summoner.puuid
    print(puuid)
    while i < 100000:
        match_list = watcher.match.matchlist_by_puuid(region, puuid)
        for match in match_list:
            match_info = watcher.match.by_id(region, match)
            for participant in match_info["metadata"]["participants"]:
                summoner_in_db = Summoner.query.filter_by(puuid=participant).first()
                if summoner_in_db is None:
                    name = watcher.summoner.by_puuid(region, participant)["name"]
                    new_summoner = Summoner(puuid=participant, nickname=name)
                    db.session.add(new_summoner)
                    game_in_db = Game.query.filter_by(game_id=match).first()
                    if game_in_db is not None:
                        new_summoner.games.append(game_in_db)
                    else:
                        new_summoner.games.append(Game(game_id=match))
                    db.session.commit()
        i += 1
        summoner = Summoner.query.filter_by(id=i).first()
        puuid = summoner.puuid
        print(puuid, i)       
    return print('End of crawling data')


def proplayers():
    site = mwclient.Site('lol.fandom.com', path='/')
    response = site.api(
        'cargoquery', 
        limit = 'max', 
        tables = "Players", 
        fields="Player, Name, Age, Team, Role, SoloqueueIds, IsRetired",
        where="SoloqueueIds IS NOT NULL")
    parsed = json.dumps(response)
    decoded = json.loads(parsed)
    return decoded


def proplayers_into_db():
    site = mwclient.Site('lol.fandom.com', path='/')
    response = site.api(
        'cargoquery', 
        limit = 'max', 
        tables = "Players", 
        fields="Player, Name, Age, Team, Role, SoloqueueIds, IsRetired",
        where="SoloqueueIds IS NOT NULL")
    parsed = json.dumps(response)
    decoded = json.loads(parsed)
    for player in decoded["cargoquery"]:
        new_player = Proplayers(
            player=player["Player"], 
            name=player["Name"], 
            age=player["Age"], 
            team=player["Team"], 
            role=player["Role"], 
            soloqueueids=player["SoloqueueIds"], 
            isretired=player["IsRetired"]
        )
        db.session.add(new_player)
        db.session.commit()
        return print('end')


if __name__ == "__main__":
    print("Script started")
    watcher = LolWatcher(KEY)
    match_id2 = "EUW1_6101420783"
    puuid1 = "A5GXIOsZv-IcgQIrrvKaASxeFw_RxVDLA1MW1PrNW-64iyW9fZtrzhfaxk4cyf-6LAuaKsA7oe7ipg"
    region = "ru"
    player1 = "StePanzer"
    player2 = "MrNoct"
    with app.app_context():
        db.create_all()
        crawling_data("ru")
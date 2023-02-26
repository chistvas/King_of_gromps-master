import mwclient
import json
import time
from riotwatcher import LolWatcher
from application import db
from application.search_engine.models import Summoner, Game, Proplayers
from config_riot import KEY


def live_data(player_nickname, region_name):
    watcher = LolWatcher(KEY)
    player = watcher.summoner.by_name(region_name, player_nickname)
    match_data = watcher.spectator.by_summoner(region_name, player["puuid"])
    return match_data
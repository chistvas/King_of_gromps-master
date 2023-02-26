from datetime import datetime
from application import db


summoner_game = db.Table('summoner_game',
    db.Column('summoner_id', db.Integer, db.ForeignKey('summoner.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

summoner_game_ru = db.Table('summoner_game_ru',
    db.Column('summoner_id', db.Integer, db.ForeignKey('summoner_ru.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game_ru.id'), primary_key=True)
)

class Summoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puuid = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    games = db.relationship("Game", secondary=summoner_game, backref='participants')

    def __repr__(self):
        return f"Summoner('{self.puuid}')"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return f"Game('{self.game_id}')"

class Proplayers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    team = db.Column(db.String(30))
    role = db.Column(db.String(30))
    soloqueueids = db.Column(db.String(30))
    isretired = db.Column(db.Integer)

    def __repr__(self):
        return f"Proplayers('{self.Player}')"

class Summoner_ru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puuid = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    games = db.relationship("Game_ru", secondary=summoner_game_ru, backref='participants_ru')

    def __repr__(self):
        return f"Summoner('{self.puuid}')"

class Game_ru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(30), nullable=False)

 
    def __repr__(self):
        return f"Game('{self.game_id}')"
import mwclient
site = mwclient.Site('lol.fandom.com', path='/')

response = site.api('cargoquery',
	limit = 'max',
	tables = "ScoreboardGames=SG",
	fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2"
)
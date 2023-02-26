from flask import Blueprint
from flask import render_template, request
from application.search_engine.scripts_search import two_players_search, collapsed_table_info


search_engine = Blueprint('search_engine', __name__)

@search_engine.route("/search_two_players")
def search():
    return render_template('search.html', title='Search two players')

@search_engine.route("/search_result", methods=['POST', 'GET'])
def search_result():
    if request.method == 'GET':
        return f"The URL /search_result is accessed directly. Try going to '/home' to submit form"
    if request.method == "POST":
        player1 = request.form.get("player1")
        player2 = request.form.get("player2")
        region = request.form.get("region")
        all_info = {}
        for match in two_players_search(player1, player2, region):
            for match_id in match:
                all_info[match_id] = collapsed_table_info(player1, region, match_id)
        return render_template(
            'search_result.html',
            title='Search result',
            player1=player1,
            player2=player2,
            region=region,
            data=all_info
            )
    return render_template('search.html')

@search_engine.route("/live")
def live_game():
    return render_template('live.html', title='Live Game')

@search_engine.route("/live_result", methods=['POST'])
def live_game_result():
    player = request.form.get("player")
    region = request.form.get("region")
    
    return render_template('live_result.html', title='Live Game Result')

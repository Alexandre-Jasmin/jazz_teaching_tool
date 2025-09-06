from flask import Blueprint, render_template, request, jsonify
from .services import load_classroom, get_summoner, get_match_data

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/classroom")
def classroom_home():
    return render_template("classroom.html")

#@main.route("/classroom/id/<string:classroom_id>")

@main.route("/lol")
def league_home():
    return render_template("league_home.html", data = 0)

@main.route("/lol/summoner")
def summoner_api():
    try:
        server = request.args.get("server", "na1")
        summoner_name = request.args.get("summoner")
        data = get_summoner(summoner_name, server)
    except Exception as e:
        return "summoner_api error"
    return jsonify(data)

@main.route("/lol/match/<string:match_id>")
def match_api(match_id):
    data = get_match_data(match_id)
    return jsonify(data)
from flask import Blueprint, render_template, request, jsonify
from .services import load_classroom, get_summoner

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/classroom")
def classroom_home():
    return render_template("classroom.html")

@main.route("/classroom/id")
def classroom_api():
    try:
        puuid = request.args.get("classroom_puuid")
        myClassroom = load_classroom(puuid)
    except Exception as e:
        return "classroom_api() error"
    return render_template("index.html", data = myClassroom)

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
        return "summoner_api() error"
    return jsonify(data)
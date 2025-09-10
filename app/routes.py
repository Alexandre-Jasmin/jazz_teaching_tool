from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
from .services import load_classroom, get_summoner, get_match_data
from .errors import SummonerNotFound, MatchNotFound
from config import Config
import markdown, os

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/docs")
def show_documentation():
    content = Config.load_docs()
    html = markdown.markdown(content)
    return render_template("docs.html", content=html)

@main.route("/classroom")
def classroom_home():
    return render_template("classroom.html")

@main.route("/lol")
def league_home():
    return render_template("league_home.html")

@main.route("/lol/search", methods=["POST"])
def find_summoner():
    server = request.form.get("server")
    summoner_name = request.form.get("summoner")
    return redirect(url_for("main.summoner_api", server=server, summoner_name=summoner_name))

@main.route("/lol/summoner/<server>/<summoner_name>")
def summoner_api(server: str, summoner_name: str):
    try:
        playerSummoner = get_summoner(summoner_name, server)
        return render_template("player_home.html", data=playerSummoner)
    except SummonerNotFound as e:
        return render_template("error.html", message=str(e)), 404
    except Exception as e:
        return render_template("error.html", message=str(e)), 500

@main.route("/lol/match/<match_id>")
def lol_match_api(match_id: str):
    try:
        myMatch = get_match_data(match_id)
        return render_template("match_information.html", data=myMatch)
    except MatchNotFound as e:
        return render_template("error.html", message=str(e)), 404
    except Exception as e:
        return render_template("error.html", message=str(e)), 500
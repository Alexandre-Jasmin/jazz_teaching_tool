from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .services import load_classroom, get_summoner

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/classroom")
def classroom_home():
    return render_template("classroom.html")

@main.route("/lol")
def league_home():
    return render_template("league_home.html")

#* Receives information from form -> summoner_api
@main.route("/lol/search", methods=["POST"])
def find_summoner():
    server = request.form.get("server")
    summoner_name = request.form.get("summoner")
    return redirect(url_for("main.summoner_api", server=server, summoner_name=summoner_name))

#* Gets LeaguePlayer and returns profile page
@main.route("/lol/summoner/<server>/<summoner_name>")
def summoner_api(server: str, summoner_name: str):
    try:
        playerSummoner = get_summoner(summoner_name, server)
    except Exception as e:
        return f"summoner_api() error: {e}"
    return render_template("player_home.html", data=playerSummoner)

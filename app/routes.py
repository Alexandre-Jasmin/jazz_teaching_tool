from flask import Blueprint, render_template, request, jsonify
from .services import load_classroom, get_summoner

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/classroom")
def classroom_api():
    classroom = load_classroom()
    return render_template("classroom.html", data=classroom.kwargs)

@main.route("/lol")
def league_home():
    # will manage how the summoner_name string is sent to summoner_api
    return "league_tool_home_page"

@main.route("/lol/summoner/<string:summoner_name>")
def summoner_api(summoner_name):
    server = request.args.get("server", "na1")
    data = get_summoner(summoner_name, server)
    return jsonify(data)
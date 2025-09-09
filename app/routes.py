from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
from .services import load_classroom, get_summoner
from config import Config
import markdown, os

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/docs")
def show_documentation():
    doc_path = os.path.join(Config.BASE_DIR, "documentation.md")
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
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
    playerSummoner = get_summoner(summoner_name, server)
    return render_template("player_home.html", data=playerSummoner)
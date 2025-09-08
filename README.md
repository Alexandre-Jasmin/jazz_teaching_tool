# jaZZ Tool

*"Personal Flask Website"*

---

## Features

- **Classroom**
  - Manage classroom data
  - Uses a basic JSON database with backup
- **League of Legends API**
  - REST endpoints:
    - `/lol/summoner`
    - `/lol/match`

---

## Structure

- **run.py**
- **config.py**
- **app/**
  - static/
  - models/
  - templates/
  - `routes.py`
  - `services.py`
- **data/**

Great question ⚡ — and here’s the key:

In Flask/Jinja, when you pass an object to a template, you’re only sending **data**, not the actual Python object with its methods. The template is rendered into static HTML/JS before it reaches the browser.

So you **cannot directly call `myObject.some_function()` from a button click** in the template.

---

### ✅ How to do it properly

You need a **Flask route** that calls the function on the server, then a **button** in the template that triggers that route (via link, form, or AJAX).

---

### Example

**In your object:**

```python
class LeaguePlayer:
    def __init__(self, name):
        self.data = {"name": name, "puuid": "12345"}

    def refresh_stats(self):
        # Do something (fetch from Riot API, etc.)
        return f"Stats refreshed for {self.data['name']}"
```

---

**Flask route (`routes.py`):**

```python
from flask import Blueprint, render_template, redirect, url_for
from app.models.player import LeaguePlayer

main = Blueprint("main", __name__)

# Pretend we store a single player
player = LeaguePlayer("Ahri")

@main.route("/player")
def player_home():
    return render_template("player_home.html", player=player)

@main.route("/player/refresh")
def refresh_player():
    result = player.refresh_stats()
    # Redirect back to page (or render JSON if using AJAX)
    return redirect(url_for("main.player_home"))
```

---

**Template (`player_home.html`):**

```html
<h2>{{ player.data["name"] }}</h2>
<p>PUUID: {{ player.data["puuid"] }}</p>

<!-- Button to trigger Flask route -->
<form action="{{ url_for('main.refresh_player') }}" method="get">
    <button type="submit">Refresh Stats</button>
</form>
```

---

### 🔄 Optional: Use JavaScript (AJAX/Fetch)

Instead of reloading the page, you can hit `/player/refresh` with JS and update part of the page dynamically.

---

⚡ **Summary:**

* Templates can **show data** but can’t call Python methods directly.
* You expose a **route in Flask** that runs the function.
* Your **button** calls that route.

---

👉 Do you want me to show you the **AJAX version** (button updates stats on the page without refreshing)?

@main.route("/lol/search", methods=["POST"])
def find_summoner():
    server = request.form.get("server")
    summoner_name = request.form.get("summoner")
    return redirect(url_for("main.summoner_api", server=server, summoner_name=summoner_name))

@main.route("/lol/summoners/<server>/<summoner_name>")
def summoner_api(server, summoner_name):
    try:
        data = get_summoner(summoner_name, server)
    except Exception as e:
        return f"summoner_api() error: {e}"
    return render_template("player_home.html", data=data)

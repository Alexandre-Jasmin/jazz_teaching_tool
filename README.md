
# jaZZ tool

*"Personnal Flask Website"*

## ✨ Features
- Classroom 
- League of Legends API

### Classroom

### League of Legends API

- Basic json database with backup
- Endpoints
- /lol/summoner
- /lol/match

# Project Structure

jazz_teaching_tool/
	.env
        .gitattributes
        .gitignore
        config.py
        LICENSE
        README.md
        requirements.txt
        run.py
        app/
            __init__.py
            routes.py
            services.py
            models/
                __init__.py
                classroom.py
                riot_api.py
                utils.py
            static/
            templates/
                base.html
                classroom.html
                index.html
                league_home.html
        data/
            classroom.pkl
            test.json
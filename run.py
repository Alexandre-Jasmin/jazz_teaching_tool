# this is the entry point
# calls flask and creates the app
from app import create_app # looks in -> __init__.py

app = create_app() # __init__.py

if __name__ == "__main__":
    app.run(debug=True, port=8000)
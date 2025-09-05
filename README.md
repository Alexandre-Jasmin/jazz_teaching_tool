You run python run.py.

run.py calls create_app() from app/__init__.py.

create_app() builds a Flask app, loads config, registers routes.

Flask starts and listens for requests.

Request comes in:

/ → handled by routes.index → calls services.create_sample_classroom() → returns HTML.

/api/classroom → handled by routes.classroom_api → returns JSON from Classroom.to_dict().
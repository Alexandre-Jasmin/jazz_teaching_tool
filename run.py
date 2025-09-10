#import subprocess
from app import create_app

app = create_app()

if __name__ == "__main__":
    #ngrok = subprocess.Popen(["ngrok", "http", "8000"])
    try:
        app.run(host="0.0.0.0", port=8000)
    finally:
        print("Flask App Terminated")
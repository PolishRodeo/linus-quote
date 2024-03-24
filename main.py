from flask import Flask, render_template, jsonify
import json
from datetime import datetime, timedelta
import random
import requests
import os

app = Flask(__name__, static_url_path='/static')

def update_quote():
    """
    Update the current quote with a random quote from the data list.
    """
    global current_quote
    current_quote = random.choice(data)
    global next_update_time
    next_update_time += timedelta(days=1)

def time_until_midnight():
    """
    Calculate the time remaining until midnight.
    Returns the time in the format HH:MM:SS.
    """
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    time_remaining = midnight - now
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# wczytaj ok?
with open("quotes.json") as file:
    data = json.load(file)
current_quote = random.choice(data)
next_update_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

@app.route("/")
def root():
    """
    Render the index.html template with the current quote, a random image, and the time remaining until midnight.
    """
    static_folder = os.path.join(os.getcwd(), 'static')
    files = [f for f in os.listdir(static_folder) if os.path.isfile(os.path.join(static_folder, f))]
    random_image = random.choice(files)
    
    response = requests.get("http://localhost:8888/api/qotd")
    data_from_api = response.json()
    requests.get("http://localhost:8888/api/time")
    qotd = jsonify({'quote': data_from_api['quote']})
    return render_template('index.html', quote=current_quote, random_image=random_image, time_until_midnight=time_until_midnight())

@app.route("/api")
def apiroot():
    """
    Welcome message for the Linus-Quotes API.
    """
    return {"message": "Welcome to Linus-Quotes API."}

@app.route('/api/qotd')
def quoteapi():
    """
    Get the quote of the day.
    If the current time is past the next update time, update the quote.
    """
    if datetime.now() >= next_update_time:
        update_quote()
    return {"quote": current_quote}

@app.route('/api/time')
def get_time():
    """
    Get the time remaining until midnight and the format of the time.
    """
    return {"next_update_in": time_until_midnight(), "format": "HH|MM|SS"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8888)

app = Flask(__name__)

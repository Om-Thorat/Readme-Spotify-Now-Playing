# Contributions From Aaron Gearheart

from flask import Flask, Response, render_template, redirect
import spotipy
from spotipy import util
import base64
import requests
import random

CLIENT_ID = "YOUR_SPOTIFY_TOKEN"
CLIENT_SECRET = "YOUR_SPOTIFY_SECRET"

scope = "user-read-playback-state user-read-recently-played"
redirect_uri = "http://127.0.0.1:5000/spotify"

app = Flask(__name__)

token = util.prompt_for_user_token("", scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
print(token)
sp = spotipy.Spotify(auth=token)

def get_info():
    try:
        current = (sp.current_playback())
        songname = (current['item']['name'])
        artist = (current['item']['artists'][0]['name'])
        cover = (current['item']['album']['images'][0]['url'])
        return ["Now Playing",songname,cover,artist]
    except:
        current = sp.current_user_recently_played(limit=1)
        songname = (current['items'][0]['track']['name'])
        artist = (current['items'][0]['track']['artists'][0]['name'])
        cover = (current['items'][0]['track']['album']['images'][0]['url'])
        return ["Last Played",songname,cover,artist]
    
@app.route('/authorize')
def authorize():
    global token
    token = util.prompt_for_user_token("", scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
    return redirect("/authorized")

@app.route('/authorized')
def authorized():
    return render_template('authorized.html')

@app.route('/spotify')
def create_image():
        info = get_info()
        print(info)
        songname = info[1].replace("&","&amp;")
        artist = info[3].replace("&","&amp;")
        response = requests.get(info[2])
        imgstr = base64.b64encode(response.content).decode()
        bars = ""
        for i in range(0,32):
            bars = bars + (f'<div class="bar" style="animation-delay: {random.randint(500,800)}ms; animation-duration: {random.randint(800,1000)}ms"></div>')
        data = {
            "status" : info[0],
            "songname":songname,
            "artist":artist,
            "imgstr":imgstr,
            "bars":bars
        }
        aight = render_template("card.html.j2",**data)
        response = Response(aight,mimetype='image/svg+xml')
        response.headers['Cache-Control'] = 'public, max-age=0, must-revalidate'
        return response

@app.route('/')
def render_homepage():
    return render_template('index.html')

app.run(debug=True)
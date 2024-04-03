from flask import Flask,Response,request,redirect,render_template
import spotipy
from spotipy import util
from pathlib import Path
import re
import base64
from PIL import Image
import requests
from io import BytesIO
import random
from spotipy import oauth2
import os

cwd = Path.cwd()
cwd = re.sub(r"\\",r"/",str(cwd))
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
scope = "user-read-playback-state user-read-recently-played"
redirect_uri = "http://127.0.0.1:5000/spotify"

app = Flask(__name__)
try:
    Refresh = os.environ['REFRESH']
    data = {
        "grant_type": "refresh_token",
        "refresh_token": Refresh,
        }

    res = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": Refresh,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    token = res.json()['access_token']
except:
    token = util.prompt_for_user_token("",scope, CLIENT_ID, CLIENT_SECRET, redirect_uri,cache_path=f"token.json")
sp = spotipy.Spotify(auth=token)
def spotify():
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
        return ["last played",songname,cover,artist]
    
@app.route('/')
def hi():
     return "Um?"

@app.route('/spotify')
def cool():
        info = spotify()
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
        resp = Response(aight,mimetype='image/svg+xml')
        resp.headers['Cache-Control'] = 'public, max-age=0, must-revalidate'
        return resp


# app.run(debug=True)
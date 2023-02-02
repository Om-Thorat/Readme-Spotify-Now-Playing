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

cwd = Path.cwd()
cwd = re.sub(r"\\",r"/",str(cwd))
CLIENT_ID = 'XXXX'
CLIENT_SECRET = 'XXXX'
username = "XXXX"
scope = "user-read-playback-state user-read-recently-played"
redirect_uri = "http://127.0.0.1:5000/"

app = Flask(__name__)
sp_oauth = oauth2.SpotifyOAuth( CLIENT_ID, CLIENT_SECRET,redirect_uri,scope=scope,cache_path=f"{cwd}/tmp/token.txt")

def spotify():
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri,cache_path=f"{cwd}/tmp/token.txt")
    sp = spotipy.Spotify(auth=token)
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
def index(): 
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return redirect("/spotify?")

    else:
        auth_url = sp_oauth.get_authorize_url()
        htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
        return htmlLoginButton


@app.route('/spotify')
def cool():
        info = spotify()
        print(info)
        songname = info[1].replace("&","&amp;")
        artist = info[3].replace("&","&amp;")
        response = requests.get(info[2])
        img = Image.open(BytesIO(response.content))
        img.save(f"{cwd}/tmp/haha",format="JPEG")
        with open(f"{cwd}/tmp/haha","rb") as img_file:
            imgstr = base64.b64encode(img_file.read()).decode()
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

app.run(debug=True)
# SVG Spotify widget 🎶

![](https://notom.deta.dev/spotify)

## Set up

You will need to make a Spotify Application first  
To do so visit [Spotify Developer portal](https://developer.spotify.com/dashboard/applications)  
login if you haven't 
Then hit create App

![](./assets/create.png)
Fill out the name and the Description and click create.

Click Edit Settings and add `http://127.0.0.1:5000` to the redirect URIs  
(P.s don't forget to scroll down and click save)

![](./assets/redirecturi.png)

Now Copy the Client ID and The Client Secret

![](./assets/creds.png)


Clone the Github Repo

``` git clone https://github.com/Om-Thorat/Readme-Spotify-Now-Playing.git```

Now move into the folder

```cd Readme-Spotify-Now-Playing```

Install the dependencies

```pip install requirements.txt```

Make a tmp directory 

```mkdir tmp```

Now paste the Credentials you copied into their respective places in your main.py file

Now run the Main.py file and visit `localhost:5000` click on sign in and **voila!** you have your own svg spotify widget.

You can now host it anywhere you wish Deploy it to [deta]("https://deta.sh") or [Vercel]("https://vercel.com)

To use it in your readme's just link to your hosting url /spotify  
for example:
```![](https://{yoururl}.vercel.app/spotify)```
similarly ```![](https://{yoururl}.deta.dev/spotify)```

Thanks,
💖 Happy Coding.

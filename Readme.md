# SVG Spotify widget 🎶

![If you see this try reloading the page!](https://notom.vercel.app/spotify)

## Set up 👀

* You will need to make a Spotify Application first To do so visit [Spotify Developer portal](https://developer.spotify.com/dashboard/applications)  
* Login and then hit create App

![](./assets/create.png)

* Fill out the name and the Description and click create.

* Click Edit Settings and add `http://127.0.0.1:5000/spotify` to the redirect URIs  
(P.s don't forget to scroll down and click save)

* Now Copy the Client ID and The Client Secret

![](./assets/creds.png)

* Fork this Repo

* Clone the Github Repo

``` git clone https://github.com/Om-Thorat/Readme-Spotify-Now-Playing.git```

* Now move into the folder

```cd Readme-Spotify-Now-Playing```

* Install the dependencies

```pip install -r requirements.txt```

* Now paste the Credentials you copied into their respective places in your index.py file located at `/api/main.py`

( ⚠️ make sure not to commit this repo with this sensitive info)

Click save and **voila!** you have your own svg spotify widget 🎉
As long as the flask app is running it will work on your computer.

You can also deploy to Vercel just make sure to add the Vercel link to your Spotify Redirect URI's

To use it in your readme's just link to your hosting url /spotify.

Thanks,
💖 Happy Coding.

## Contributions
Thanks to [AaronGearheart](https://github.com/AaronGearheart) for

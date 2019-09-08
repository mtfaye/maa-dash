# maa-dash
Analytical music application, built using the analytic web app framework, Dash and powered by the Spotify web api.
![ezgif com-video-to-gif](https://user-images.githubusercontent.com/39230255/64483326-ddba8480-d1cd-11e9-9cc8-81f793c359a1.gif)

## Repo contents:

- app.py : This is the main front-end and back-end application code. Contains the dash application layouts, graphs coding, callbacks for interactivities of the app, interfaces with the database...

- requirement.txt: Contains all the dependencies. 
- assets: contains all the statics images and CSS Boostrap codes.
- spotify.data.db: sqlite database, no need to use this file. You can create the file in your directory by simply running the app.py



## Running the app:

- Clone the repo
- Install requirements by using pip install -r requirements.txt.
- Sign up on Spotify for free if you do not have an account already and go to https://developer.spotify.com/dashboard/login, fill in the form and get your spotify app credentials.

- Use the wrapper Spotipy to set up your terminal variables:
            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

            Get your credentials at     
                https://developer.spotify.com/my-applications

- Run on a local server

 
## Credits
A big shoutout to all the open source codes like Dash and Spotipy that made this app easier for me to develop.

## Enjoy!

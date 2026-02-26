# Simple script to sync all playlists from Spotify to Saavn
Uses OAuth for Spotify and Cookie for Saavn (No legit API available, so sign into Saavn, copy the cookie in Requests header tab and put in the .env file)
You need to have Spotify Premium to make an app on it and get client_credentials😭

## Setup
Add client_id, client_secret and redirect_uri of your Spotify App created from Spotify Developer dashoard {https://developer.spotify.com/dashboard}.
Add Cookie from Saavn Web App's DevTools

Install dependencies using poetry
```bash
poetry install
```

Run main.py:
```bash
poetry run python main.py
```

NOTE : This runs into error if any duplicate playlist_name is encountered.


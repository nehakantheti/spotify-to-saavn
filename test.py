from src.spotify_to_saavn.spotify import SpotifyClient
s = SpotifyClient()
print(s.sp.current_user())   # should return your user profile JSON
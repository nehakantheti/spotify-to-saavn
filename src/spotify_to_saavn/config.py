import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888")

# Capture response['results']['id'] & response['results']['language'] -- will be usd in adding to a playlist in contents
# SEARCH_BASE_URL=https://www.jiosaavn.com/api.php?__call=search.getResults&_format=json&_marker=0&cc=in&p=1&n=20&q=
SEARCH_BASE_URL='https://www.jiosaavn.com/api.php?__call=search.getResults&_format=json&_marker=0&cc=in&p=1&n=20&q='  # add search with space replaced by + 
# Capture the listid to put in add to plalist endpoint
CREATE_PLAYLIST_BASE_URL='https://www.jiosaavn.com/api.php?__call=playlist.create&share=true&api_version=4&_format=json&ctx=wap6dot4' # add &listname=<listname>
# Accepting only single song per request, dont why th its that way//
# format for contents=~~<song_id>~<song_language>
# ADD_TO_PLAYLIST_BASE_URL='https://www.jiosaavn.com/api.php?__call=playlist.add&api_version=4&_format=json&_marker=0&ctx=wap6dot0&listid=1298191649&contents=' # ~~cLWnfq9s~hindi
# ADD_TO_PLAYLIST_BASE_URL='https://www.jiosaavn.com/api.php?__call=playlist.add&api_version=4&_format=json&_marker=0&ctx=wap6dot0&contents=' # ~~cLWnfq9s~hindi # add listid as well
ADD_TO_PLAYLIST_BASE_URL='https://www.jiosaavn.com/api.php?__call=playlist.add&api_version=4&_format=json&_marker=0&ctx=web6dot0' # &listid=1298200534&contents=~~Omr4_8bG~hindi%5E~~544D8U6a~hindi%5E~~Zg8B9cap~hindi%5E~~CaAvIaC4~hindi%5E~~uzKP2W4Z~hindi%5E~~P5uK7hT0~hindi%5E~~P9gnb-lE~hindi%5E~~D7kPILrg~hindi%5E~~ZXgYn8Wr~hindi%5E~~8-1G5_Vt~hindi%5E~~5EbcfiS5~hindi%5E~~W4kteoV-~hindi
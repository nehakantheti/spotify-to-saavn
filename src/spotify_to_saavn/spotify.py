import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.spotify_to_saavn import config
# import os
# from dotenv import load_dotenv
from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)
# load_dotenv()

# client_id = os.getenv("SPOTIFY_CLIENT_ID")
# client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
# redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

class SpotifyClient:
    def __init__(self):
        logger.info("Initializing Spotify Client Class")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=config.SPOTIPY_CLIENT_ID,
            client_secret=config.SPOTIPY_CLIENT_SECRET,
            redirect_uri=config.SPOTIPY_REDIRECT_URI,
            scope="playlist-read-private"
        ))

        logger.info("Spotify Client initialization completed successfully!")

    def get_user_playlists(self):
        logger.debug("Fetching user playlists from Spotify API.")
        try:
            results = self.sp.current_user_playlists()
            playlists = results.get('items', [])
            logger.info(f"Successfully fetched {len(playlists)} playlists.")
            return playlists
        except Exception as e:
            logger.error(f"Error fetching playlists: {e}", exc_info=True)
            raise

    def get_playlist_tracks(self, playlist_id: str) -> list:
        logger.debug(f"Fetching tracks for playlist {playlist_id}")
        try:
            # spotipy's method to get tracks in a playlist
            tracks = self.sp.playlist_items(playlist_id)
            parsed_tracks = []

            while tracks:   # run till pagination calls are valid
                for item in tracks.get('items', []):
                    track_data = item.get('track')
                    
                    if not track_data:
                        # If track_data is null, continue with next item
                        continue

                    artists = track_data.get('artists', []) # default to empty list
                    artist_name = artists[0]['name'] if artists else 'Unknown Track'

                    parsed_tracks.append({
                        'name': track_data.get('name', 'Unknown Track'),
                        'artist': artist_name,
                        # ISRC (Internationsal Standard Recording Code) used to find tracks uniquely
                        'isrc': track_data.get('external_ids', {}).get('isrc')
                    })

                if tracks.get('next'):
                    logger.debug('Fetching next page of tracks...')
                    tracks = self.sp.next(tracks)
                else:
                    tracks=None

            logger.info(f"Successfully extracted {len(parsed_tracks)} tracks from playlist {playlist_id}")
            return parsed_tracks
            
        except Exception as e:
            logger.error(f"Error fetching tracks of playlist {playlist_id} : {e}", exc_info=True)
            raise

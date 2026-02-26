import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)

class SpotifyClient:
    def __init__(self):
        logger.info("Initializing Spotify Client Class")
        # Load .env (if present) so env vars are available when running helpers/tests
        load_dotenv()

        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

        # logger.info(f'{client_id}\n{client_secret}\n{redirect_uri}')

        if not client_id or not client_secret or not redirect_uri:
            logger.error("Missing Spotify credentials. Ensure SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URI are set in the environment or .env file.")
            raise RuntimeError("Missing Spotify credentials: set SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URI")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-read-private playlist-read-collaborative"
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

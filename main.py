import os
from pathlib import Path
from src.spotify_to_saavn.logger import setup_logger
from dotenv import load_dotenv

from src.spotify_to_saavn.spotify import SpotifyClient
from src.spotify_to_saavn.saavn import SaavnClient
from src.spotify_to_saavn.transfer import TransferManager

logger = setup_logger(__name__)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    saavn_cookie = os.getenv("SAAVN_COOKIE")

    if not saavn_cookie:
        logger.error(f'SAAVN_COOKIE is missing. Please add it to the .env file from website afte log in. (Find it the Applications tab of DevTools).')
        return
    
    logger.info(f'Initilizing clients...')

    try:
        spotify_client = SpotifyClient()
        saavn_client = SaavnClient(auth_cookie=saavn_cookie)

        manager = TransferManager(spotify_client=spotify_client, saavn_client=saavn_client)

        logger.info('Fetching all the spotify playlists...')
        playlists = spotify_client.get_user_playlists()

        if not playlists:
            logger.warning(f'No playlists found on your Spotify account')
            return
        
        logger.info(f'Found {len(playlists)} playlists to transfer. Starting batch process...')

        for index, playlist in enumerate(playlists, start=1):
            playlist_id = playlist.get('id')
            playlist_name = playlist.get('name', f'Unknown Playlist {index}')

            logger.info(f"Processing Playlist {index}/{len(playlists)} : '{playlist_name}'")

            manager.execute_transfer(
                spotify_playlist_id=playlist_id,
                new_playlist_name=playlist_name
            )

        logger.info(f'All playlist transfers have been processed successfully')
    except Exception as e:
        logger.error(f'An unexpected error occurred during batch transfer: {e}', exc_info=True)

if __name__=="__main__":
    main()
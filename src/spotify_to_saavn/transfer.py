from src.spotify_to_saavn.logger import setup_logger
from pprint import pprint
import re

logger = setup_logger(__name__)

class TransferManager:
    def __init__(self, spotify_client, saavn_client):
        self.spotify = spotify_client
        self.saavn = saavn_client
        logger.info("Initialized TransferManager Successfully!")

    def sanitize_query(self, query):
        # Remove extra info in parentheses/quotes, extra whitespace
        query = re.sub(r'\s*\(.*?\)\s*', '', query)
        query = re.sub(r'\s*".*?"\s*', '', query)
        query = query.strip()
        return query

                                                                  #dict[song_id, language], missing_tracks
    def get_jiosaavn_track_ids(self, spotify_playlist_id: str) -> tuple[dict, list[dict]]:
        """Takes a Spotify Playlist ID and return a tuple of
        1. A list of matched JioSaavn track IDs - TrackID is a string, so its a list[string]
        2. A list of tracks that could not be found - Track is a dictionary, so returns a list[dict]
        """

        logger.info(f"Starting track matching for Spotify Playlist: {spotify_playlist_id}")

        # get tracks from spotify client
        spotify_tracks = self.spotify.get_playlist_tracks(spotify_playlist_id)

        # pprint(spotify_tracks)

        # saavn ids of the matched tracks
        matched_saavn_ids = {}
        
        # missing tracks will be dicts
        missing_tracks = []

        for track in spotify_tracks:
            # search query with both name and artis
            query = self.sanitize_query(f"{track['name']} {track['artist']}")

            # invoking search with the saavn instance
            saavn_result = self.saavn.search_song(query)

            if saavn_result is None:
                logger.warning(f"Skipping track, no match found: {query}")
                missing_tracks.append(query)
                continue  # Skip this track

            # logger.warning(f"{saavn_result}")
            # pprint(saavn_result)

            song_id = saavn_result['id']
            song_language = saavn_result['language']
            song_name = saavn_result['song']
            song_album = saavn_result['album']
            if saavn_result and song_id and song_language:
                # appending only id of saavn track found
                # appending as a tuple
                matched_saavn_ids[song_id] = song_language
                logger.info(f'Found Match in transfer file : {song_id} with language {song_language}')
                logger.info(f'Found Match in transfer file : {song_name} from  {song_album}')
            else:
                logger.warning(f"Could not find match for : {track['name']} by {track['artist']}")
                # adding the whole track info to missing_tracks
                missing_tracks.append(track)

        logger.info(f"Matching complete. Found {len(matched_saavn_ids)} tracks. Missed {len(missing_tracks)} tracks.")
        return matched_saavn_ids, missing_tracks
    
    def execute_transfer(self, spotify_playlist_id: str, new_playlist_name: str) -> bool:
        """Return True if the operation is successful else false"""
        logger.info(f'Starting full transfer for spotify playlist {spotify_playlist_id} to Saavn with playlist name {new_playlist_name}')

        matched_ids, missing_tracks = self.get_jiosaavn_track_ids(spotify_playlist_id)

        if not matched_ids:
            logger.error(f"No tracks were matched on Saavn. Aborting transfer")
            return False
        
        new_playlist_id = self.saavn.create_playlist(new_playlist_name)
        if not new_playlist_id:
            logger.error(f"Error encountered while creating a new playlist with name {new_playlist_name}")
            return False
        
        # ADd only matched ids to the new playlist created
        success = self.saavn.add_songs_to_playlist(new_playlist_id, matched_ids)

        if success:
            logger.info(f"Transfer from spotify playlist {spotify_playlist_id} to new playlist with id {new_playlist_id} on Saavn is successful!\n")
            if missing_tracks:
                logger.warning(f'{len(missing_tracks)} tracks are missing on saavn in the playlist {new_playlist_id} - Not added to the saavn playlist with id {new_playlist_id}')
                return True
        else:
            logger.error(f'Failed to add songs to the newly created playlist on saavn.')
            return False
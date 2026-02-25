from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)

class TransferManager:
    def __init__(self, spotify_client, saavn_client):
        self.spotify = spotify_client
        self.saavn = saavn_client
        logger.info("Initialized TransferManager Successfully!")

    def get_jiosaavn_track_ids(self, spotify_playlist_id: str) -> tuple[list[str], list[dict]]:
        """Takes a Spotify Playlist ID and return a tuple of
        1. A list of matched JioSaavn track IDs - TrackID is a string, so its a list[string]
        2. A list of tracks that could not be found - Track is a dictionary, so returns a list[dict]
        """

        logger.info(f"Starting track matching for Spotify Playlist: {spotify_playlist_id}")

        # get tracks from spotify client
        spotify_tracks = self.spotify.get_playlist_tracks(spotify_playlist_id)

        # saavn ids of the matched tracks
        matched_saavn_ids = []
        
        # missing tracks will be dicts
        missing_tracks = []

        for track in spotify_tracks:
            # search query with both name and artis
            query = f"{track['name']} {track['artist']}"

            # invoking search with the saavn instance
            saavn_result = self.saavn.search_song(query)

            if saavn_result and saavn_result.get('id'):
                # appending only id of saavn track found
                matched_saavn_ids.append(saavn_result["id"])
            else:
                logger.warning(f"Could not find match for : {track['name']} by {track['artist']}")
                # adding the whole track info to missing_tracks
                missing_tracks.append(track)

        logger.info(f"Matching complete. Found {len(matched_saavn_ids)} tracks. Missed {len(missing_tracks)} tracks.")
        return matched_saavn_ids, missing_tracks
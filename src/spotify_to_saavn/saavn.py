import requests
from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)

class SaavnClient:
    def __init__(self, auth_cookie: str = None):
        self.api_base = "https://saavn.me"  # Base URL for the wrapper
        self.search_url = f"{self.api_base}/search/songs"
        self.auth_cookie = auth_cookie
        logger.info("Initializing JioSaavn Client...")

    def search_song(self, query: str) -> dict | None:
        logger.debug(f"Searching JioSaavn for : {query}")
        try: 
            response = requests.get(self.search_url, params={"query": query})

            # raises an exception if the status_code is 4xx or 5xx
            response.raise_for_status()

            data = response.json()  # converting into json
            results = data.get("results", [])

            if not results:
                logger.warning(f"No results found on JioSaavn for the query {query}")
                return None
            
            top_result = results[0]
            logger.info(f"Found match : {top_result.get('title')} by {top_result.get('singers')}")

            return top_result


        except Exception as e:
            logger.error(f"HTTP error while searching for a song with query {query} : {e}", exc_info=True)
            return None
        except ValueError:
            logger.error(f"Failed to parse JSON response for query: {query}", exc_info=True)
            return None
        
    def create_playlist(self, name: str) -> str | None:
        if not self.auth_cookie:
            logger.error(f"Auth Cookie not set, ran into ValueError : {e}", exc_info=True)
            raise ValueError("Authentication cookie is required to modify user data")
        
        logger.info(f"Creating Saavn Playlist {name}")

        try:
            headers = {"Cookie": self.auth_cookie}
            payload = {"title": name}

            response = requests.post(f'{self.api_base}/playlists', json=payload, headers=headers)
            response.raise_for_status()

            playlist_id = response.json().get("data", {}).get('id')
            return playlist_id

        except Exception as e:
            logger.error(f"Error encountered while creating playlist '{name}': {e}", exc_info=True)
            return None
        
    # Returns only the status of song addition to playlist
    def add_songs_to_playlist(self, playlist_id: str, song_ids: list[str]) -> bool:
        if not self.auth_cookie:
            logger.error(f"Auth Cookie is not set, ran into Value Error : {e}", exc_info=True)
            raise ValueError("Authentication cookie is required to modify user data")
        logger.info(f"Adding {len(song_ids)} to playlist {playlist_id}")

        try:
            headers = {"Cookie": self.auth_cookie}
            payload = {'song_ids': song_ids}

            # assuming a put endpoint to update playlist contents
            response = requests.put(f"{self.api_base}/playlists/{playlist_id}", json=payload, headers=headers)
            response.raise_for_status

            logger.info(f"Successfully added {len(song_ids)} to playlist {playlist_id}")
            return True
        except Exception as e:
            logger.error(f'Error encountered while adding songs to playlist {playlist_id}')
            return False
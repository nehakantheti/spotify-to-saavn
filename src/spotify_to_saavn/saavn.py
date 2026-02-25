import requests
from src.spotify_to_saavn.logger import setup_logger
from pprint import pprint
from src.spotify_to_saavn.config import SEARCH_BASE_URL, CREATE_PLAYLIST_BASE_URL, ADD_TO_PLAYLIST_BASE_URL
from urllib.parse import urlencode

logger = setup_logger(__name__)

class SaavnClient:
    def __init__(self, auth_cookie: str = None):
        # self.api_base = "https://saavn.me"  # Base URL for the wrapper
        # self.search_url = f"{self.api_base}/search/songs"
        self.search_url = SEARCH_BASE_URL
        self.auth_cookie = auth_cookie
        logger.info("Initializing JioSaavn Client...")

    def encode_search_string(self, inp: str) -> str:
        return inp.replace(' ', '+')

    def search_song(self, query: str) -> dict | None:
        logger.debug(f"Searching JioSaavn for : {query}")
        headers = {"Cookie": self.auth_cookie}
        try: 
            url = self.search_url + self.encode_search_string(query)
            response = requests.get(url, headers=headers)

            # raises an exception if the status_code is 4xx or 5xx
            # pprint(response)
            response.raise_for_status()

            data = response.json()  # converting into json
            results = data.get("results", [])

            if not results:
                logger.warning(f"No results found on JioSaavn for the query {query}")
                return None
            
            top_result = results[0]
            logger.info(f"Found match : {top_result.get('song')} by {top_result.get('primary_artists')}")

            return top_result
        except Exception as e:
            logger.error(f"HTTP error while searching for a song with query {query} : {e}", exc_info=True)
            return None
        except ValueError:
            # logger.error(f"Failed to parse JSON response for query: {query}", exc_info=True)
            # return None
            logger.error(f"Failed to parse JSON response for query: {query}")
            # ADD THIS LINE to see the actual error from the server
            logger.error(f"Raw API Response: {response.text}") 
            return None
        
    def create_playlist(self, name: str) -> str | None:
        if not self.auth_cookie:
            logger.error(f"Auth Cookie not set, ran into ValueError", exc_info=True)
            raise ValueError("Authentication cookie is required to modify user data")
        
        logger.info(f"Creating Saavn Playlist {name}")

        try:
            headers = {"Cookie": self.auth_cookie}
            payload = {"title": name}

            # response = requests.post(f'{self.api_base}/playlists', json=payload, headers=headers)
            url = CREATE_PLAYLIST_BASE_URL + f'&listname={name}'
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            # print(f'Response of create playlist : \n')
            pprint(response)
            
            data = response.json() #.get("details", {}).get('listid')
            # logger.info(f'Response : {data}')
            playlist_id = data['details']['id']
            
            # logger.info(f'New ID : {playlist_id}')
            return playlist_id

        except Exception as e:
            logger.error(f"Error encountered while creating playlist '{name}': {e}", exc_info=True)
            return None
        
    # Returns only the status of song addition to playlist
    def add_songs_to_playlist(self, playlist_id: str, song_ids: dict) -> bool:
        if not self.auth_cookie:
            logger.error(f"Auth Cookie is not set, ran into Value Error", exc_info=True)
            raise ValueError("Authentication cookie is required to modify user data")
        logger.info(f"Adding {len(song_ids)} to playlist {playlist_id}")

        url= ADD_TO_PLAYLIST_BASE_URL + f"&listid={playlist_id}"
        content_vals = ''
        for key, value in song_ids.items():
            content_vals += f"~~{key}~{value}%5E"
        content_vals[:-3]
        url += f"&contents={content_vals}"
        try:
            headers = {"Cookie": self.auth_cookie}
            # payload = {'song_ids': song_ids}

            # assuming a put endpoint to update playlist contents
            # response = requests.put(f"{self.api_base}/playlists/{playlist_id}", json=payload, headers=headers)
            response = requests.get(url, headers=headers)
            response.raise_for_status
            logger.info(response)
            logger.info(f"Successfully added {len(song_ids)} songs to playlist {playlist_id}")
            return True
        except Exception as e:
            logger.error(f'Error encountered while adding songs to playlist {playlist_id} : {e}', exc_info=True)
            return False
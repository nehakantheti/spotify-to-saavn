import requests
from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)

class SaavnClient:
    def __init__(self):
        self.search_url = "https://saavn.me/search/songs"
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
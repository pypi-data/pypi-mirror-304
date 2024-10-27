from typing import Optional, List
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from jikanapi.models import Anime
import time
from rich import print


class JikanAPI:
    def __init__(self, max_tries: int = 10):
        self.jikan = Jikan()
        self.max_tries = max_tries

    def get_anime(self, anime_id: int) -> Optional[Anime]:
        for attempt in range(self.max_tries):
            try:
                data = self.jikan.anime(anime_id)["data"]
                return Anime(**data)
            except APIException as e:
                if "RateLimitException" in str(e):
                    print(
                        "[bold blue]Rate limit exceeded. Waiting for 3 seconds before retrying...[/bold blue]"
                    )
                    print(
                        f"[bold blue]Retry: ({attempt + 1}/{self.max_tries}) [/bold blue]"
                    )
                    time.sleep(3)
                elif "HTTP 404" in str(e):
                    print(f"Anime with ID {anime_id} not found.")
                    return
                else:
                    raise e
            except Exception as e:
                raise e

        raise RuntimeError("Max retries reached. Could not retrieve anime.")

    def search_anime(self, query: str) -> List[Anime]:
        for attempt in range(self.max_tries):
            try:
                search_results = self.jikan.search("anime", query)["data"]
                return [Anime(**anime) for anime in search_results]
            except APIException as e:
                if "RateLimitException" in str(e):
                    print(
                        "[bold blue]Rate limit exceeded. Waiting for 3 seconds before retrying...[/bold blue]"
                    )
                    print(
                        f"[bold blue]Retry: ({attempt + 1}/{self.max_tries}) [/bold blue]"
                    )
                    time.sleep(3)
                else:
                    raise e
            except Exception as e:
                raise e

        raise RuntimeError("Max retries reached. Could not perform search.")

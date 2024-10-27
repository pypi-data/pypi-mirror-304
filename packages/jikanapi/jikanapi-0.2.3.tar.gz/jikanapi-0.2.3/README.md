# JikanAPI (In Development)

JikanAPI is a Python wrapper for the [Jikan API](https://jikan.moe/), designed to provide an easy-to-use interface for accessing anime data from MyAnimeList (MAL). It enhances the standard jikanpy-v4 package by adding features like automatic handling of rate limits, improved error messages, and structured data models.

## Development Status

This project is currently in development. New features will be added in the future, including support for Manga and more.

## Features

- **Automatic Rate Limit Handling**: Automatically waits for 3 seconds when hitting rate limits and retries the request.
- **Error Handling**: Provides clear messages for different types of errors, including HTTP 404 for missing anime.
- **Data Models**: Utilizes Pydantic for structured and validated data models, ensuring that the returned data conforms to expected types.
- **Enhanced Information**: Returns detailed information about anime, including genres, producers, licensors, studios, themes, images, and trailers.

## Installation

You can install JikanAPI via pip:

```bash
pip install jikanapi
```

## Usage

Here's an example of how to use JikanAPI to get information about an anime:

```python
from jikanapi import JikanAPI
from rich import print

jikan_client = JikanAPI()
anime_data = jikan_client.get_anime(44511)
print(anime_data)

```

### Sample Output

When you run the above code, you might see output similar to this:

```py
Anime(
    mal_id=44511,
    url='https://myanimelist.net/anime/44511/Chainsaw_Man',
    title='Chainsaw Man',
    title_japanese='チェンソーマン',
    title_english='Chainsaw Man',
    title_synonyms=[],
    type='TV',
    source='Manga',
    episodes=12,
    status='Finished Airing',
    airing=False,
    aired=Aired(
        from_date='2022-10-12T00:00:00+00:00',
        to_date='2022-12-28T00:00:00+00:00',
        string='Oct 12, 2022 to Dec 28, 2022'
    ),
    duration='24 min per ep',
    rating='R - 17+ (violence & profanity)',
    score=8.48,
    scored_by=910588,
    rank=151,
    popularity=70,
    members=1629913,
    favorites=48710,
    synopsis="""Denji is robbed of a normal teenage life, left with nothing but his deadbeat father's
overwhelming debt. His only companion is his pet, the chainsaw devil Pochita, with whom he slays devils for
money that inevitably ends up in the yakuza's pockets. All Denji can do is dream of a good, simple life: one
with delicious food and a beautiful girlfriend by his side. But an act of greedy betrayal by the yakuza leads
to Denji's brutal, untimely death, crushing all hope of him ever achieving happiness.\n\nRemarkably, an old
contract allows Pochita to merge with the deceased Denji and bestow devil powers on him, changing him into a
hybrid able to transform his body parts into chainsaws. Because Denji's new abilities pose a significant risk
to society, the Public Safety Bureau's elite devil hunter Makima takes him in, letting him live as long as he
obeys her command. Guided by the promise of a content life alongside an attractive woman, Denji devotes
everything and fights with all his might to make his naive dreams a reality""",
    background='Chainsaw Man was released in four volumes on Blu-ray and DVD from January 27, 2023 to April 28,
2023. It adapts chapters 1-38 of the original manga.',
    season='fall',
    year=2022,
    genres=[
        Genre(mal_id=1, name='Action', type='anime', url='https://myanimelist.net/anime/genre/1/Action'),
        Genre(mal_id=10, name='Fantasy', type='anime', url='https://myanimelist.net/anime/genre/10/Fantasy')
    ],
    producers=[
        Producer(
            mal_id=1856,
            name='dugout',
            type='anime',
            url='https://myanimelist.net/anime/producer/1856/dugout'
        )
    ],
    licensors=[],
    studios=[
        Studio(
            mal_id=569,
            name='MAPPA',
            type='anime',
            url='https://myanimelist.net/anime/producer/569/MAPPA'
        )
    ],
    themes=[
        Theme(mal_id=58, name='Gore', type='anime', url='https://myanimelist.net/anime/genre/58/Gore'),
        Theme(
            mal_id=82,
            name='Urban Fantasy',
            type='anime',
            url='https://myanimelist.net/anime/genre/82/Urban_Fantasy'
        )
    ],
    images=Images(
        jpg=ImageUrls(
            image_url='https://cdn.myanimelist.net/images/anime/1806/126216.jpg',
            small_image_url='https://cdn.myanimelist.net/images/anime/1806/126216t.jpg',
            large_image_url='https://cdn.myanimelist.net/images/anime/1806/126216l.jpg'
        ),
        webp=ImageUrls(
            image_url='https://cdn.myanimelist.net/images/anime/1806/126216.webp',
            small_image_url='https://cdn.myanimelist.net/images/anime/1806/126216t.webp',
            large_image_url='https://cdn.myanimelist.net/images/anime/1806/126216l.webp'
        )
    ),
    trailer=Trailer(
        youtube_id='q15CRdE5Bv0',
        url='https://www.youtube.com/watch?v=q15CRdE5Bv0',
        embed_url='https://www.youtube.com/embed/q15CRdE5Bv0?enablejsapi=1&wmode=opaque&autoplay=1',
        images=TrailerImages(
            image_url='https://img.youtube.com/vi/q15CRdE5Bv0/default.jpg',
            small_image_url='https://img.youtube.com/vi/q15CRdE5Bv0/sddefault.jpg',
            medium_image_url='https://img.youtube.com/vi/q15CRdE5Bv0/mqdefault.jpg',
            large_image_url='https://img.youtube.com/vi/q15CRdE5Bv0/hqdefault.jpg',
            maximum_image_url='https://img.youtube.com/vi/q15CRdE5Bv0/maxresdefault.jpg'
        )
    )
)
```

## Differences from jikanpy-v4

1. **Rate Limit Management**: Unlike jikanpy-v4, JikanAPI automatically manages rate limiting by implementing retries with wait times, minimizing the risk of hitting rate limits during repeated requests.

2. **Error Handling**: JikanAPI provides enhanced error handling, specifically checking for rate limit exceptions and missing resources, and giving clear feedback to the user.

3. **Structured Data Models**: JikanAPI leverages Pydantic to define structured data models, making it easier to work with and validate the response data from the API.

4. **Rich Output**: Integration with the Rich library for improved console output, making debugging and logging more visually appealing.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

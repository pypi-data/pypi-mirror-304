from pydantic import BaseModel, Field
from typing import List, Optional


class Genre(BaseModel):
    mal_id: int
    name: str
    type: str
    url: str


class Producer(BaseModel):
    mal_id: int
    name: str
    type: str
    url: str


class Licensor(BaseModel):
    mal_id: int
    name: str
    type: str
    url: str


class Studio(BaseModel):
    mal_id: int
    name: str
    type: str
    url: str


class Theme(BaseModel):
    mal_id: int
    name: str
    type: str
    url: str


class AiredDate(BaseModel):
    day: int
    month: int
    year: int


class Aired(BaseModel):
    from_date: Optional[str] = Field(None, alias="from")
    to_date: Optional[str] = Field(None, alias="to")
    string: str

    class Config:
        populate_by_name = True


class ImageUrls(BaseModel):
    image_url: str
    small_image_url: str
    large_image_url: str


class Images(BaseModel):
    jpg: ImageUrls
    webp: ImageUrls


class TrailerImages(BaseModel):
    image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    medium_image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    maximum_image_url: Optional[str] = None


class Trailer(BaseModel):
    youtube_id: Optional[str] = None
    url: Optional[str] = None
    embed_url: Optional[str] = None
    images: TrailerImages


class Anime(BaseModel):
    mal_id: int
    url: str
    title: str
    title_japanese: Optional[str]
    title_english: Optional[str]
    title_synonyms: List[str]
    type: Optional[str]
    source: Optional[str]
    episodes: Optional[int]
    status: Optional[str]
    airing: bool
    aired: Aired
    duration: Optional[str]
    rating: Optional[str]
    score: Optional[float]
    scored_by: Optional[int]
    rank: Optional[int]
    popularity: Optional[int]
    members: Optional[int]
    favorites: Optional[int]
    synopsis: Optional[str]
    background: Optional[str]
    season: Optional[str]
    year: Optional[int]
    genres: List[Genre]
    producers: List[Producer]
    licensors: List[Licensor]
    studios: List[Studio]
    themes: List[Theme]
    images: Images
    trailer: Trailer

    class Config:
        populate_by_name = True

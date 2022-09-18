from datetime import datetime
from typing import List, Optional

from attrs import define, field

from shiki4py.types.anime import Anime
from shiki4py.types.user_rate_full import UserRateFull


@define
class AnimeProfile(Anime):
    rating: Optional[str]
    english: List[Optional[str]]
    japanese: List[Optional[str]]
    synonyms: List[Optional[str]]
    license_name_ru: Optional[str]
    duration: int
    description: Optional[str]
    description_html: Optional[str]
    description_source: Optional[str]
    franchise: Optional[str]
    favoured: bool
    anons: bool
    ongoing: bool
    thread_id: Optional[int]
    topic_id: Optional[int]
    myanimelist_id: Optional[int]
    rates_scores_stats: List[dict]
    rates_statuses_stats: List[dict]
    updated_at: datetime = field(repr=str)
    next_episode_at: Optional[datetime] = field(repr=str)
    fansubbers: List[str]
    fandubbers: List[str]
    licensors: List[str]
    genres: List[dict]
    studios: List[dict]
    videos: List[dict]
    screenshots: List[dict]
    user_rate: Optional[UserRateFull]

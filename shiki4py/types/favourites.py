from typing import List

from attrs import define

from shiki4py.types.favourite import Favourite


@define
class Favourites:
    animes: List[Favourite]
    mangas: List[Favourite]
    ranobe: List[Favourite]
    characters: List[Favourite]
    people: List[Favourite]
    mangakas: List[Favourite]
    seyu: List[Favourite]
    producers: List[Favourite]

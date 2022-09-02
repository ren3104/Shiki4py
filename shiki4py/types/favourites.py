from typing import List

from attrs import define, field

from shiki4py.types.favourite import Favourite


@define
class Favourites:
    animes: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    mangas: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    ranobe: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    characters: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    people: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    mangakas: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    seyu: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])
    producers: List[Favourite] = field(converter=lambda l: [Favourite(**d) for d in l])

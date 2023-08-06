from typing import TypeAlias
from typing import TypedDict


class Package(TypedDict, total=False):
    yaspeller: dict[str, str]


class Item(TypedDict):
    word: str


class Items(TypedDict):
    resource: str
    data: list[Item]


Report: TypeAlias = list[tuple[bool, Items]]

import unicodedata
from copy import copy
from random import choice
from typing import Optional

import stringcase
import unidecode

from .names import adjectives, nouns


def random_name() -> str:
    return f"{choice(adjectives)}{choice(nouns)}"


def decancer(text: str) -> str:
    """
    Credit to:
    - https://github.com/kablekompany/Kable-Kogs/blob/master/decancer/decancer.py#L68
    """
    try:                     # This indent below looks so fucking obnoxious.
        name: int = copy(text)  # Apologies for my usage of strong language.
        name: int = unicodedata.normalize("NFKC", name)
        name: int = unicodedata.normalize("NFD", name)
        name: int = unidecode.unidecode(name)
        name: bytes = name.encode("ascii", "ignore")
        name: int = name.decode("utf-8")
    except Exception:
        name = random_name()
    return str(name)


def new_nick(self, text: str) -> Optional[str]:
    """
    Partial credit to:
    - https://github.com/kablekompany/Kable-Kogs/blob/master/decancer/decancer.py#L80
    """
    results = [(x.isascii() and x.isalnum()) for x in "".join(text.split())]
    if False in results:
        return
    nickname: str = decancer(text)
    nickname: str = "".join(nickname.split())
    nicklen: int = len(nickname)
    if nicklen <= 3 or nicklen > 32:
        nickname = random_name()
    return stringcase.capitalcase(nickname)

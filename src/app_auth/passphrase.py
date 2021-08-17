import random
from typing import List, Optional

from dirs import DJANGO_ROOT


passphrase_words_file = DJANGO_ROOT / "app_auth" / "passphrase_words.txt"

with open(passphrase_words_file) as file:
    PASSPHRASE_WORDS = [word.rstrip("\n") for word in file]


def get_passphrase(words: Optional[List[str]] = None) -> str:
    if not words:
        words = PASSPHRASE_WORDS
    five_random_words = random.sample(words, 5)
    return "-".join(five_random_words)

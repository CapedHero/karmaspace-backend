import re

from text_unidecode import unidecode


def get_cleaned_username(username: str) -> str:
    temp = unidecode(username)
    temp = re.sub(r"[^\w\s-]", "", temp).strip()
    temp = re.sub(r"[-\s]+", "-", temp)
    return temp

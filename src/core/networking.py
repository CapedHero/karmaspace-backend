import functools

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.core import time_units


session = requests.Session()

session.request = functools.partial(session.request, timeout=time_units.in_s.SEC_30)

# Below will result in retries after 0.25, 0.5, 1, 2, 4, 8, and 16 seconds.
retry_strategy = Retry(
    total=7,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

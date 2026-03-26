import requests
from django.core.cache import cache

BASE_URL = "https://api.artic.edu/api/v1/artworks"


def fetch_artwork(external_id: int):
    cache_key = f"artwork:{external_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    response = requests.get(f"{BASE_URL}/{external_id}", timeout=5)
    if response.status_code != 200:
        return None

    data = response.json().get("data")
    if not data:
        return None

    result = {
        "external_id": data["id"],
        "title": data.get("title", f"Artwork {data['id']}")
    }
    cache.set(cache_key, result, timeout=60 * 60)
    return result
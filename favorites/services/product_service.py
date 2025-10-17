import httpx
from django.core.cache import cache

FAKESTORE_BASE = "https://fakestoreapi.com/products/"

def get_product(product_id: int):
    key = f"product:{product_id}"
    if (data := cache.get(key)):
        return data

    try:
        response = httpx.get(f"{FAKESTORE_BASE}{product_id}", timeout=5.0)
        if response.status_code == 200:
            cache.set(key, response.json(), timeout=300)  # 5 min
            return response.json()
    except httpx.RequestError:
        return None

from .api_client import get


def products_find_all():
    return get("/product")

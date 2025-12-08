from .api_client import get, put


def products_find_all():
    return get("/product")


def prodcut_update_quantity(id, quantity):
    return put("/product/" + str(id) + "/quantity", {"quantity": quantity})

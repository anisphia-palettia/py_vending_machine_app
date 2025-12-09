from .api_client import get, put, post, post_file, post_multipart


def products_find_all():
    return get("/product")


def product_update_quantity(id, quantity):
    return put("/product/" + str(id) + "/quantity", {"quantity": quantity})


def product_create(name, slug, price, quantity, image_path=None):
    # Endpoint: POST /product (multipart/form-data)
    payload = {
        "name": name,
        "slug": slug,
        "price": str(price),
        "quantity": str(quantity),
    }

    if image_path:
        # We need to keep file open during request.
        # Using a context manager inside would be tricky if we return the response.
        # But requests.post executes immediately.
        try:
            with open(image_path, "rb") as f:
                return post_multipart("/product", data=payload, files={"image": f})
        except Exception as e:
            return {"success": False, "message": f"File error: {str(e)}"}

    return post_multipart("/product", data=payload)


def product_update(id, data):
    # data: {name, slug, price, quantity, image}
    return put("/product/" + str(id), data)


def upload_image(file_path):
    with open(file_path, "rb") as f:
        # Assuming endpoint is /product/upload
        return post_file("/product/upload", files={"file": f})

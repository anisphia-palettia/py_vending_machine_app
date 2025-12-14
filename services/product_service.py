from .api_client import get, put, post, post_file, post_multipart, put_multipart, delete


def products_find_all():
    return get("/product")


def product_update_quantity(id, quantity):
    return put("/product/" + str(id) + "/quantity", {"quantity": quantity})


def product_create(name, price, quantity, image_path=None):
    # Endpoint: POST /product (multipart/form-data)
    payload = {
        "name": name,
        "price": str(price),
        "quantity": str(quantity),
    }

    if image_path:
        try:
            with open(image_path, "rb") as f:
                return post_multipart("/product", data=payload, files={"image": f})
        except Exception as e:
            return {"success": False, "message": f"File error: {str(e)}"}

    return post_multipart("/product", data=payload)


def product_update(id, name, price, quantity, image_path=None):
    # Endpoint: PUT /product/<id> (multipart/form-data)
    payload = {
        "name": name,
        "price": str(price),
        "quantity": str(quantity),
    }

    if image_path:
        try:
            with open(image_path, "rb") as f:
                return put_multipart(
                    "/product/" + str(id), data=payload, files={"image": f}
                )
        except Exception as e:
            return {"success": False, "message": f"File error: {str(e)}"}

    return put_multipart("/product/" + str(id), data=payload)


def upload_image(file_path):
    with open(file_path, "rb") as f:
        # Assuming endpoint is /product/upload
        return post_file("/product/upload", files={"file": f})


def product_delete(id):
    return delete("/product/" + str(id))

from .api_client import post

def login(username, password):
    return post("/auth/login", {"username": username, "password": password})
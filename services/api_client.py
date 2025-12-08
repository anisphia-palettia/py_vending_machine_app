import requests
from core.config import API_URL


def get(path):
    return requests.get(API_URL + path).json()


def post(path, data):
    return requests.post(API_URL + path, json=data).json()


def put(path, data):
    return requests.put(API_URL + path, json=data).json()


def delete(path):
    return requests.delete(API_URL + path).json()

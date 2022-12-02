from enum import Enum


class MethodType(str, Enum):
    get = "GET"
    put = "PUT"
    post = "POST"
    delete = "DELETE"

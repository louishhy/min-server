from typing import Callable, Dict
from request import HTTPRequest
from response import HTTPResponse

class MiddlewareManager:
    def __init__(self):
        self.request_middlewares: list[Callable] = []
        self.response_middlewares: list[Callable] = []

    def process_request(self, request):
        for middleware in self.request_middlewares:
            middleware(request)

    def process_response(self, response):
        for middleware in self.response_middlewares:
            middleware(response)

    def add_request_middleware(self, middleware):
        self.request_middlewares.append(middleware)

    def add_response_middleware(self, middleware):
        self.response_middlewares.append(middleware)


class CookieParser:
    def __call__(self, request: HTTPRequest):
        cookie_header = request.headers.get("Cookie", "")
        cookies: Dict[str, str] = {}
        for cookie in cookie_header.split(";"):
            key, value = cookie.split("=")
            cookies[key.strip()] = value.strip()
        request.cookies = cookies
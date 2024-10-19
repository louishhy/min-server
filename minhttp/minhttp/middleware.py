from typing import Callable

from request import HTTPRequest


class MiddlewareManager:
    def __init__(self):
        self.request_middlewares: list[Callable] = []
        self.response_middlewares: list[Callable] = []

    def process_request(self, request):
        for middleware in self.request_middlewares:
            middleware_resp = middleware(request)
            if middleware_resp:
                return middleware_resp

    def process_response(self, response):
        for middleware in self.response_middlewares:
            middleware_resp = middleware(response)
            if middleware_resp:
                return middleware_resp

    def add_request_middleware(self, middleware):
        self.request_middlewares.append(middleware)

    def add_response_middleware(self, middleware):
        self.response_middlewares.append(middleware)


class CookieParser:
    def __call__(self, request: HTTPRequest):
        cookie_header = request.headers.get("Cookie", "")
        cookies: dict[str, str] = {}
        for cookie in cookie_header.split(";"):
            key, value = cookie.split("=")
            cookies[key.strip()] = value.strip()
        request.cookies = cookies

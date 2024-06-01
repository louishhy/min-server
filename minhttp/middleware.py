from typing import Callable

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
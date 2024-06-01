from typing import Callable, Optional
from request import HTTPRequest
from response import HTTPResponse, text

class Router:
    def __init__(self, 
                 default_handler: Optional[Callable[[HTTPRequest], HTTPResponse]] = None):
        self.routes: list[tuple[str, str, Callable]] = []
        self.default_handler = self._default_handler \
            if default_handler is None else default_handler

    def route(self, request: HTTPRequest) -> Callable[[HTTPRequest], HTTPResponse]:
        for method, path, handler in self.routes:
            if method == request.method and self.pattern_match(path, request.path):
                return handler
        return self.default_handler
    
    def pattern_match(self, pattern: str, path: str) -> bool:
        # Now we implement a very naive one
        return pattern == path
    
    def _default_handler(self, request: HTTPRequest) -> HTTPResponse:
        return text(body = "Not Found", status_code=404, reason="Not Found")
        
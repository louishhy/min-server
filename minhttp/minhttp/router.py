from dataclasses import dataclass, field
from typing import Callable, Optional

from request import HTTPRequest
from response import HTTPResponse
from utils import text_response


@dataclass
class PatternMatchResult:
    matched: bool
    params: dict[str, str] = field(default_factory=dict)


class Router:
    def __init__(
        self, default_handler: Optional[Callable[[HTTPRequest], HTTPResponse]] = None
    ):
        self.routes: list[tuple[str, str, Callable]] = []
        self.default_handler = (
            self._default_handler if default_handler is None else default_handler
        )

    def route(self, request: HTTPRequest) -> Callable[[HTTPRequest], HTTPResponse]:
        for method, path, handler in self.routes:
            pattern_match_result = self.pattern_match(path, request.path)
            if method == request.method and pattern_match_result.matched:
                # Populate the request parameters, if any
                request.params = pattern_match_result.params
                return handler
        return self.default_handler

    def add_route(self, method: str, path: str, handler: Callable):
        self.routes.append((method, path, handler))

    def pattern_match(self, pattern: str, path: str) -> PatternMatchResult:
        # Check if there are any angle brackets in the pattern
        if "<" not in pattern:
            return PatternMatchResult(matched=(pattern == path), params={})
        else:
            return self._pattern_match_with_params(pattern, path)

    def _default_handler(self, request: HTTPRequest) -> HTTPResponse:
        return text_response(body="Not Found", status_code=404, reason="Not Found")

    def _pattern_match_with_params(self, pattern: str, path: str) -> PatternMatchResult:
        # Split the pattern and path by the forward slash
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")
        # Match the length of the parts
        if len(pattern_parts) != len(path_parts):
            return PatternMatchResult(matched=False, params={})
        # Match one-by-one until a mismatch is found or pattern encounters a '<>'
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if "<" in pattern_part:
                break
            if pattern_part != path_part:
                return PatternMatchResult(matched=False, params={})
        # Extract the parameters from the pattern
        params = {}
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            # Failsafe
            if pattern_part[0] != "<" or pattern_part[-1] != ">":
                raise ValueError(f"Invalid angle bracket pattern: {pattern}")
            params[pattern_part[1:-1]] = path_part
        return PatternMatchResult(matched=True, params=params)
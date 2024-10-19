import urllib
import urllib.parse
from dataclasses import dataclass, field


@dataclass  # dataclass make your code more clean
class HTTPRequest:
    method: str
    path: str
    query: dict[str, list[str]]
    version: str
    headers: dict[str, str]
    body: str
    params: dict[str, str] = field(default_factory=dict)
    cookies: dict[str, str] = field(default_factory=dict)

    def __init__(self, http_str: str):
        http_str_lines = http_str.split("\r\n")
        request_line = http_str_lines[0]
        self.headers = dict()
        self.body = ""
        # Parse request line
        self.method, request_uri, self.version = HTTPRequest._parse_request_line(
            request_line
        )
        # Parse headers
        parse_cursor = 1
        while http_str_lines[parse_cursor] != "":
            key, value = HTTPRequest._parse_header_line(http_str_lines[parse_cursor])
            self.headers[key] = value
            parse_cursor += 1
        # Parse body if present
        parse_cursor = parse_cursor + 1
        if parse_cursor < len(http_str_lines):
            self.body = "\r\n".join(http_str_lines[parse_cursor:])
        self.path, self.query = HTTPRequest._parse_request_uri(request_uri)

    def __str__(self) -> str:
        return f"HTTPRequest({str(self.__dict__)})"

    @staticmethod
    def _parse_request_line(request_line):
        parts = request_line.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid HTTP request line: {request_line}")
        return parts[0], parts[1], parts[2]

    @staticmethod
    def _parse_header_line(header_line):
        parts = header_line.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HTTP header line: {header_line}")
        return parts[0].strip(), parts[1].strip()

    @staticmethod
    def _parse_request_uri(request_uri: str):
        parsed = urllib.parse.urlparse(request_uri)
        return parsed.path, urllib.parse.parse_qs(parsed.query)

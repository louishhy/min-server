import urllib
import urllib.parse

class HTTPRequest:
    def __init__(self, method: str,
                 request_uri: str,
                 version: str,
                 headers: dict[str, str],
                 body: str):
        self.method = method
        # Parse the request uri
        self.path, self.query = HTTPRequest._parse_request_uri(request_uri)
        self.version = version
        self.headers = headers
        self.body = body
        self.params = dict()

    def __str__(self):
        return f"HTTPRequest({str(self.__dict__)})"
    
    @staticmethod
    def parse_http_str(http_str: str):
        http_str_lines = http_str.split("\r\n")
        request_line = http_str_lines[0]
        headers: dict[str, str] = dict()
        body = ""
        # Parse request line
        method, request_uri, version = HTTPRequest._parse_request_line(request_line)
        # Parse headers
        parse_cursor = 1
        while http_str_lines[parse_cursor] != "":
            key, value = HTTPRequest._parse_header_line(http_str_lines[parse_cursor])
            headers[key] = value
            parse_cursor += 1
        # Parse body if present
        parse_cursor = parse_cursor + 1
        if parse_cursor < len(http_str_lines):
            body = "\r\n".join(http_str_lines[parse_cursor:])
        # Return object
        return HTTPRequest(method=method, request_uri=request_uri, version=version, headers=headers, body=body)

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

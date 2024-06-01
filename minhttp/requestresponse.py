class HTTPResponse:
    def __init__(self, status_code=200, reason="OK"):
        self.status_code = status_code
        self.reason = reason
        self.headers = {
            "Server": "SimpleHTTP/0.1",
            "Content-Type": "text/plain",
            "Connection": "close",
        }
        self.body = ""

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body
        self.headers["Content-Length"] = str(len(body))
    
    def to_string(self):
        response_line = f"HTTP/1.1 {self.status_code} {self.reason}\r\n"
        headers = "".join(f"{key}: {self.headers[key]}\r\n" for key in self.headers)
        httpstr = response_line + headers + "\r\n" + self.body
        return httpstr

    def to_bytes(self):
        httpstr = self.to_string()
        return httpstr.encode("utf-8")


class HTTPRequest:
    def __init__(self, method: str,
                 path: str,
                 version: str,
                 headers: dict[str, str],
                 body: str):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
    
    @staticmethod
    def parse_http_str(http_str: str):
        http_str_lines = http_str.split("\r\n")
        request_line = http_str_lines[0]
        headers: dict[str, str] = dict()
        body = ""
        # Parse request line
        method, path, version = HTTPRequest._parse_request_line(request_line)
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
        return HTTPRequest(method=method, path=path, version=version, headers=headers, body=body)

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

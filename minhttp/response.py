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


# Helper functions to help you quickly create a response
def text(body, status_code=200, reason="OK"):
    response = HTTPResponse(status_code, reason)
    response.set_header("Content-Type", "text/plain")
    response.set_body(body)
    return response
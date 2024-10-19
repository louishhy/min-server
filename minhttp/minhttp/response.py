import json
from dataclasses import dataclass, field
from typing import Dict

from version import VERSION


@dataclass
class HTTPResponse:
    status_code: int = 200
    reason: str = "OK"
    headers: Dict[str, str] = field(
        default_factory=lambda: {
            "Server": f"MinHTTP/{VERSION}",
            "Content-Type": "text/plain",
            "Connection": "close",
        }
    )
    body: str = ""

    def set_header(self, key: str, value: str):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body
        self.headers["Content-Length"] = str(len(body))

    def __str__(self):
        response_line = f"HTTP/1.1 {self.status_code} {self.reason}\r\n"
        headers = "".join(f"{key}: {self.headers[key]}\r\n" for key in self.headers)
        httpstr = response_line + headers + "\r\n" + self.body
        return httpstr

    def to_bytes(self):
        return self.__str__().encode("utf-8")


# Helper functions to help you quickly create a response
def text_response(body, status_code=200, reason="OK") -> HTTPResponse:
    response = HTTPResponse(status_code, reason)
    response.set_header("Content-Type", "text/plain")
    response.set_body(body)
    return response


def json_response(body_dict: dict, status_code=200, reason="OK") -> HTTPResponse:
    response = HTTPResponse(status_code, reason)
    response.set_header("Content-Type", "application/json")
    response.set_body(json.dumps(body_dict))
    return response


def html_response(body, status_code=200, reason="OK") -> HTTPResponse:
    response = HTTPResponse(status_code, reason)
    response.set_header("Content-Type", "text/html")
    response.set_body(body)
    return response

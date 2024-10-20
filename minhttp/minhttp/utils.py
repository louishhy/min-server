import mimetypes
import json
import os

from minhttp.response import HTTPResponse

# Factory functions to help you quickly create a response
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


def file_response(file_path: str, status_code=200, reason="OK") -> HTTPResponse:
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine the content type using mimetypes
    content_type, _ = mimetypes.guess_type(file_path)
    
    if content_type is None:
        content_type = "application/octet-stream"  # Default to binary if type is unknown

    # Read the file contents, raises OSError for reading
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Create an HTTP response with the file content
    response = HTTPResponse(status_code, reason)
    response.set_header("Content-Type", content_type)
    response.set_body(file_content.decode("utf-8") if "text" in content_type else file_content)
    return response


def internal_error_response(msg: str = "Internal Server Error") -> HTTPResponse:
    return text_response(msg, status_code=500, reason="Internal Server Error")
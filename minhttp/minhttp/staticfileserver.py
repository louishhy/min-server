import os

from minhttp.request import HTTPRequest
from minhttp.utils import file_response, text_response

class StaticFileServer:
    def __init__(self, root_dir: str = "static"):
        self.root_dir = root_dir

    def serve_static_file(self, request: HTTPRequest):
        requested_filename = request.path.lstrip("/static/")
        file_path = os.path.join(self.root_dir, requested_filename)
        try:
            # Craft a file response
            return file_response(file_path)
        except FileNotFoundError:
            # Return a plain 404 response for demo purposes
            return text_response("Not Found", status_code=404, reason="Not Not Found")
        
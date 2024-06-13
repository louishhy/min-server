import minhttpserver
from response import text_response
from middleware import CookieParser

host, port = "localhost", 8080

"""
If you would like to activate SSL, make sure:
1. You set ssl_enabled=True in the MinHTTPServer constructor
2. You have generated the private key and certificate files.
For details, please refer to the README.md file.
"""
app = minhttpserver.MinHTTPServer(host, port, ssl_enabled=False)

app.middleware_manager.add_request_middleware(CookieParser())

@app.get("/check/inspect_request")
def check_your_request(request):
    return text_response(str(request))

@app.get("/check/inspect_params/<param1>")
def check_your_params(request, param1):
    return text_response(f"param1 = {param1}")

app.run()
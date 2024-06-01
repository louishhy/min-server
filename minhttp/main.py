import minhttpserver
from response import text_response
from middleware import CookieParser

host, port = "localhost", 8080

app = minhttpserver.MinHTTPServer(host, port, ssl_enabled=False)

app.middleware_manager.add_request_middleware(CookieParser())

@app.get("/check/inspect_request")
def check_your_request(request):
    return text_response(str(request))

@app.get("/check/inspect_params/<param1>/<param2>")
def check_your_params(request, param1, param2):
    return text_response(f"param1 = {param1}, param2 = {param2}")

app.run()
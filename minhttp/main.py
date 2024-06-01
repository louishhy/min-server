import minhttpserver
from response import text
from middleware import CookieParser

host, port = "localhost", 8080

app = minhttpserver.MinHTTPServer(host, port, ssl_enabled=False)

app.middleware_manager.add_request_middleware(CookieParser())

@app.get("/check/inspect_request")
def check_your_request(request):
    return text(str(request))

@app.get("/check/inspect_params/<param1>/<param2>")
def check_your_params(request, param1, param2):
    return text(f"param1 = {param1}, param2 = {param2}")

app.run()
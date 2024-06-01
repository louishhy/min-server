import minhttpserver
from response import text

host, port = "localhost", 8080

app = minhttpserver.MinHTTPServer(host, port, ssl_enabled=True)

"""
@app.get("/")
def home(request):
    return text("Hello, world!")
"""


app.run()
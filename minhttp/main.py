import minhttpserver

host, port = "localhost", 8080

app = minhttpserver.MinHTTPServer(host, port)

app.run()
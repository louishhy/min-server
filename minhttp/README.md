# MinHTTP
A minimalistic HTTP server written in Python.

## Enabling SSL/TLS
1. Install OpenSSL
2. Generate a private key.
```bash
openssl genpkey -algorithm RSA -out key.pem -aes256
```
3. Generate a self-signed certificate.
```bash
openssl req -new -x509 -key key.pem -out cert.pem -days 365
```
4. Configure your server to use SSL/TLS by setting the `ssl_enabled` parameter to `True` in the `MinHTTPServer` constructor.
```python
app = minhttpserver.MinHTTPServer(host, port, ssl_enabled=True)
```
# min-server

The `min-server` project aims to provide a series of minimalistic implementations of common server-side applications 
to help beginners understand the underlying logic of APIs by providing easy-to-understand code and [documentations](https://louishhy.github.io/min-server-docs/).

## Subprojects
### [MinHTTP](minhttp)
[Flask](https://flask.palletsprojects.com/en/3.0.x/)-like, minimalistic implementation of HTTP server from the `socket` level using only native Python libraries.

### MinWebSocket
🥳 To be implemented, stay tuned!

## Why `min-server`?
Modern server applications and frameworks are extremely sophisticated. Although those careful engineering makes them powerful and production-ready, it can be overwhelming for beginners to understand the underlying logic of server applications from the source code.

The aim of `min-server` is to cut away the complexity and focus on the core flow of server applications, such as connection establishments, routing and handling messages. By understanding the basics with the source code and documentation, you can dive into more sophisticated frameworks with ease.

> [!IMPORTANT]
>
> Because of the reasons mentioned above, `min-server` is _not_ designed for production use. Some mechanisms such as authentication are largely simplified or even omitted. 
>
> Do _not_ use `min-server` in production environments.

## Contributing
🥳 We welcome contributions to `min-server`! If you have any ideas or suggestions, feel free to open an issue or pull request.

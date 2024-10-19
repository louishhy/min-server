import logging


def log_exceptions(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            logging.exception(f"An exception occurred in function {fn.__name__}")

    return wrapper

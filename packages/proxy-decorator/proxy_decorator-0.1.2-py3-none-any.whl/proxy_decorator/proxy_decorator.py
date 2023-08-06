import os
import configparser
from functools import wraps

"""
load proxy config
"""
def load_http_proxy_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    http_proxy = config.get("http", "http")
    https_proxy = config.get("http", "https")
    username = config.get("http", "username")
    password = config.get("http", "password")

    proxy_auth = f"{username}:{password}" if username and password else None

    return http_proxy, https_proxy, proxy_auth

"""
decoretor to use http proxy from settings in config file
"""
def proxy_http(config_file):
    http_proxy, https_proxy, proxy_auth = load_http_proxy_config(config_file)
    return with_http_proxy(http_proxy, https_proxy, proxy_auth)

"""
set proxy while using. turn back to the origin proxy setting till the end.
"""
def with_http_proxy(http_proxy, https_proxy, proxy_auth=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_http_proxy = os.environ.get("HTTP_PROXY")
            original_https_proxy = os.environ.get("HTTPS_PROXY")
            if proxy_auth:
                os.environ["HTTP_PROXY"] = f"{http_proxy}/{proxy_auth}"
                os.environ["HTTPS_PROXY"] = f"{https_proxy}/{proxy_auth}"
            else:
                os.environ["HTTP_PROXY"] = http_proxy
                os.environ["HTTPS_PROXY"] = https_proxy
            try:
                result = func(*args, **kwargs)
            finally:
                if original_http_proxy is not None:
                    os.environ["HTTP_PROXY"] = original_http_proxy
                else:
                    os.environ.pop("HTTP_PROXY", None)

                if original_https_proxy is not None:
                    os.environ["HTTPS_PROXY"] = original_https_proxy
                else:
                    os.environ.pop("HTTPS_PROXY", None)
            return result
        return wrapper
    return decorator

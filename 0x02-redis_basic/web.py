#!/usr/bin/env python3
""" A caching request module
"""
import redis
import requests
from functools import wraps
from typing  import Callable, Any


def track_get_page(fn: Callable) -> Callable:
    """ getter for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        wrapper that checks if a url's data is cached
        and tracks how many times the get_page is called.
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Makes a http request to a given endpoint
    params:
        url - the url of the web page to retreive
    Returns:
        The content of the web page.
    """
    response = requests.get(url)
    return response.text

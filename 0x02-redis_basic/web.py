#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

# Create a Redis connection object
redis_store = redis.Redis()

def data_cacher(method: Callable[[str], str]) -> Callable[[str], str]:
    '''Decorator to cache the output of a method and track access count.'''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Caches the fetched result and increments the access count.'''
        
        # Increment the count for each URL access
        redis_store.incr(f'count:{url}')
        
        # Check if the result is already cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            # Return the cached result if available
            return cached_result.decode('utf-8')
        
        # Fetch the page content if not cached
        result = method(url)
        
        # Cache the result with a 10-second expiration
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return wrapper

@data_cacher
def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL and caches it.
    
    Args:
        url (str): The URL of the webpage to fetch.
        
    Returns:
        str: The content of the webpage.
    '''
    return requests.get(url).text

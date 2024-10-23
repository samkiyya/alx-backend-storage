#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

# Redis instance for caching and tracking
redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks access count.'''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.'''
        
        # Increment the access count for the URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            # If cached, return the result from cache
            return cached_result.decode('utf-8')
        
        # Fetch the page if not in cache
        result = method(url)
        
        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Fetches the content of a URL and caches the result.'''
    return requests.get(url).text

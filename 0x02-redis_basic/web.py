#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks access count.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        # Increment the count of how many times this URL has been accessed
        redis_store.incr(f'count:{url}')
        
        # Check if the result is already cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        # Fetch the page if not in cache
        result = method(url)
        
        # Cache the result with a 10 second expiration time
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text

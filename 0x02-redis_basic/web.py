#!/usr/bin/env python3
'''A module for fetching and caching web pages with access tracking.
'''

import redis
import requests
from functools import wraps
from typing import Callable

# Redis connection instance
redis_store = redis.Redis()

def cache_decorator(method: Callable) -> Callable:
    '''Decorator to cache the result of a function and track access count.'''
    
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function that manages caching and tracking of URL accesses.'''
        
        # Track how many times the URL has been accessed
        count_key = f"count:{url}"
        redis_store.incr(count_key)
        
        # Check if the URL's content is already cached
        cache_key = f"cached:{url}"
        cached_page = redis_store.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')  # Return cached content
        
        # Fetch the page content using requests
        response = requests.get(url)
        page_content = response.text
        
        # Cache the content for 10 seconds
        redis_store.setex(cache_key, 10, page_content)
        
        return page_content
    
    return wrapper

@cache_decorator
def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL.
    
    Args:
        url (str): The URL to fetch the content from.
        
    Returns:
        str: The HTML content of the URL.
    '''
    return requests.get(url).text

#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and tracker.
This module provides functionality to track URL access frequency
and cache web page content with a 10 second expiration time.
"""
import requests
import time
from functools import wraps
from typing import Dict, Callable


def count_url_access() -> Dict:
    """
    Create a dictionary to store URL access counts.
    
    Returns:
        Dict: Empty dictionary for storing URL access counts
    """
    return {}


def cache_content() -> Dict:
    """
    Create a dictionary to store cached content.
    
    Returns:
        Dict: Empty dictionary for storing cached content
    """
    return {}


cache: Dict = cache_content()
count_cache: Dict = count_url_access()


def cache_decorator(func: Callable) -> Callable:
    """
    Decorator that implements caching and URL access counting.
    
    Args:
        func: The function to be decorated that fetches web pages
        
    Returns:
        Callable: Wrapper function that adds caching and counting
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper that handles caching and counting of URL accesses.
        
        Args:
            url: The URL to fetch and cache
            
        Returns:
            str: The HTML content of the webpage
        """
        # Increment count for this URL
        count_key = f"count:{url}"
        count_cache[count_key] = count_cache.get(count_key, 0) + 1
        
        current_time = time.time()
        
        # Return cached content if still valid
        if url in cache:
            content, expiry_time = cache[url]
            if current_time < expiry_time:
                return content
            
        # Fetch and cache new content
        content = func(url)
        cache[url] = (content, current_time + 10)
        return content
    
    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    """
    Fetch and return the HTML content of a webpage.
    
    Args:
        url (str): The URL of the webpage to fetch
        
    Returns:
        str: The HTML content of the webpage
    """
    response = requests.get(url)
    return response.text
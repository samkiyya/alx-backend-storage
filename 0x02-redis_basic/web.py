#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and tracker.
This module provides functionality to cache web page content
and track the number of times a URL is accessed.
"""
import requests
import time
from functools import wraps
from typing import Dict


def cache_decorator(fn):
    """
    Decorator that implements caching and access counting for URLs.
    
    Args:
        fn: The function to be decorated
        
    Returns:
        wrapper function that implements caching and counting
    """
    cache: Dict = {}
    
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper function that handles caching and counting of URL accesses.
        
        Args:
            url: The URL to fetch and cache
            
        Returns:
            str: The content of the webpage
        """
        current_time = time.time()
        
        # Update count for the URL
        count_key = f"count:{url}"
        if count_key not in cache:
            cache[count_key] = 0
        cache[count_key] += 1
        
        # Check if cached content exists and is still valid
        if url in cache:
            content, expiry_time = cache[url]
            if current_time < expiry_time:
                return content
        
        # Fetch new content if cache missing or expired
        content = fn(url)
        cache[url] = (content, current_time + 10)  # Cache for 10 seconds
        return content
    
    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    """
    Fetches the content of a webpage and returns it.
    
    Args:
        url (str): The URL of the webpage to fetch
        
    Returns:
        str: The content of the webpage
    """
    response = requests.get(url)
    return response.text

#!/usr/bin/env python3
"""
 Cache class module
"""

import uuid
from typing import Union, Callable
import redis


class Cache:
    """Create a Cache class."""

    def __init__(self):
        """Initialize the Redis instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """Count the number of times a method is called."""
        key = method.__qualname__

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """Wrapper function."""
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """Get data from Redis."""
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Get a string from Redis."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Get an int from Redis."""
        return self.get(key, fn=int)

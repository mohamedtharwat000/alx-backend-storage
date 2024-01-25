#!/usr/bin/env python3
"""
 Cache class module
"""

import uuid
from typing import Union
import redis


class Cache:
    """Create a Cache class."""

    def __init__(self):
        """Initialize the Redis instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

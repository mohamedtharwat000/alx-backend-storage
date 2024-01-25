#!/usr/bin/env python3
""" Writing strings to Redis """
import uuid
from typing import Union, Optional, Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """ stores the count of calling the Cache class's methods """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)

        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function. """
    in_key = f'{method.__qualname__}:inputs'
    out_key = f'{method.__qualname__}:outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(in_key, str(args))

        res = method(self, *args, **kwargs)
        self._redis.rpush(out_key, res)

        return res
    return wrapper


def replay(method: Callable) -> None:
    """ display the history of calls of a particular function. """

    key = method.__qualname__
    cache = redis.Redis()
    inputs_history = cache.lrange(f'{key}:inputs', 0, -1)
    outputs_history = cache.lrange(f'{key}:outputs', 0, -1)

    print(f'{key} was called {len(inputs_history)} times:')

    for inputs, output in zip(inputs_history, outputs_history):
        inputs_str = inputs.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f'{key}(*{inputs_str}) -> {output_str}')


class Cache():
    """ doc """

    def __init__(self):
        """ init """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            store the input data in Redis using the random key
            and return the key.
        """
        id = str(uuid.uuid4())
        self._redis.set(id, data)

        return (id)

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    int,
                                                                    None]:
        """
            take a key string argument
            and an optional Callable argument named fn.
            This callable will be used to convert
            the data back to the desired format.
        """

        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """ get the string representation from the self.get method """
        data = self.get(key,
                        lambda x: x.decode('utf-8')
                        if isinstance(x, bytes)
                        else str(x))
        return str(data)

    def get_int(self, key: str) -> Union[int, str, None]:
        """ get the integer representation from the self.get method """
        data = self.get(key,
                        lambda x: int(x) if x.isdigit() else None)

        return data

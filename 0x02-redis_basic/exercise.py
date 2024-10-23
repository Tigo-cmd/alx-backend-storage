#!/usr/bin/env python3
"""this module implements interactions with redis"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_count))
    fxninputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxninput, fxn_output in zip(fxninputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxninput.decode("utf-8"),
            fxn_output,
        ))


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a class.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache:
    """ implements caching using redis"""

    def __init__(self) -> None:
        """init cache instance"""
        self.__redis: redis = redis.Redis()
        self.__redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        takes a data and returns a string, generates a random key using uuid,
        stores the input data in Redis using the random key and return the key.
        """
        randomkey = str(uuid.uuid4())
        self.__redis.set(randomkey, data)
        return randomkey

    def get(self, key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))

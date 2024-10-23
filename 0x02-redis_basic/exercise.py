#!/usr/bin/env python3
"""this module implements interactions with redis"""

import redis
import uuid
from functools import wraps
from typing import Union


class Cache:
    """ implements caching using redis"""
    def __init__(self) -> None:
        """init cache instance"""
        self.__redis: redis = redis.Redis()
        self.__redis.flushdb(True)

    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        takes a data and returns a string, generates a random key using uuid,
        stores the input data in Redis using the random key and return the key.
        """
        randomkey = str(uuid.uuid4())
        self.__redis.set(randomkey, data)
        return randomkey

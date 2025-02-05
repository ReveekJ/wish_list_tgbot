from typing import TypeVar, Type, Optional

import redis
from pydantic import BaseModel

from src.config import REDIS_HOST, REDIS_PORT

Schema = TypeVar('Schema', bound=BaseModel)


class CacheManager:
    def __init__(self, db: int, schema_class: Optional[Type[Schema]] = None):
        self.__cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
        self.__db = db
        self.__schema_class = schema_class

    def cache_set(self, key, value: Schema | dict | str | int | float | bytes):
        try:
            if isinstance(value, self.__schema_class):
                value = value.model_dump_json()
        except TypeError:
            raise TypeError(f"schema_class must be defined, not {type(self.__schema_class)}")

        self.__cache.set(key, value)

    def cache_get(self, key) -> Schema:
        if self.__schema_class is None:
            raise TypeError(f"schema_class must be defined, not {type(self.__schema_class)}")

        try:
            return self.__schema_class.model_validate_json(self.__cache.get(key))
        except ValueError:
            return self.__cache.get(key)

    def cache_delete(self, key):
        self.__cache.delete(key)

    def save_cache_from_db(self, id_field_name: str = 'id'):
        def wrapper(func):
            def inner(*args, **kwargs):
                res = func(*args, **kwargs)
                if hasattr(res, id_field_name):
                    self.cache_set(res.id, res)
                return res
            return inner
        return wrapper

    def reset_cache(self, id_field_name: str = 'id'):
        def wrapper(func):
            def inner(*args, **kwargs):
                res = func(*args, **kwargs)
                try:
                    self.cache_delete(getattr(res, id_field_name))
                except AttributeError:
                    pass
                except Exception as e:
                    print('CacheManager error', e)
                return res
            return inner
        return wrapper

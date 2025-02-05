from abc import ABC, abstractmethod
from typing import Optional, Type, List, Dict, Any, TypeVar

from pydantic import BaseModel, Field

from src.db.db_connect import get_session, Base
from src.utils.cache_manager import CacheManager

# Определяем обобщенные типы
M = TypeVar('M', bound=Base)  # Модель
S = TypeVar('S', bound=BaseModel)  # Схема


class DBParams(BaseModel):
    exclude_fields_on_creation: Optional[set[str]] = Field(default_factory=set)
    cache_redis_db: int


class DBContextManagerTemplate:
    def __init__(self):
        self._db = get_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()


class DBTemplate[M, S](DBContextManagerTemplate, CacheManager):
    def __init__(self, model_class: Type[M], schema_class: Type[S], params: DBParams):
        CacheManager.__init__(self, params.cache_redis_db, schema_class)
        super().__init__()
        self._model_class = model_class
        self._schema_class = schema_class
        self._params = params

    def create(self, obj: S) -> S:
        model = self._model_class(**obj.model_dump(exclude=self._params.exclude_fields_on_creation))
        self._db.add(model)
        self._db.commit()

        schema = self._schema_class.model_validate(model, from_attributes=True)
        return schema

    def get_obj_by_id(self, obj_id: int) -> Optional[S]:
        cached_data = self.cache_get(obj_id)  # вернет None если ключ отсутствует
        if cached_data:
            return cached_data

        obj = self._db.query(self._model_class).filter(self._model_class.id == obj_id).first()
        schema = self._schema_class.model_validate(obj, from_attributes=True) if obj else None

        return schema

    def get_all(self, skip: int = 0, limit: int = 10) -> List[S]:
        objs = self._db.query(self._model_class).offset(skip).limit(limit).all()
        return [self._schema_class.model_validate(obj, from_attributes=True) for obj in objs]

    def update(self, obj_id: int, obj_data: Dict[str, Any]) -> Optional[S]:
        obj = self._db.query(self._model_class).filter(self._model_class.id == obj_id).first()
        if obj:
            for key, value in obj_data.items():
                setattr(obj, key, value)
            self._db.commit()

            # обновляем кеш
            schema = self._schema_class.model_validate(obj, from_attributes=True)
            return schema
        return None

    def delete(self, obj_id: int) -> Optional[S]:
        obj = self._db.query(self._model_class).filter(self._model_class.id == obj_id).first()
        if obj:
            self._db.delete(obj)
            self._db.commit()

            # удаляем из кеша
            schema = self._schema_class.model_validate(obj, from_attributes=True)
            return schema
        return None

from typing import Optional, Type, List

from pydantic import BaseModel, Field

from src.db.db_connect import get_session, Base


class DBParams(BaseModel):
    exclude_fields_on_creation: Optional[set[str]] = Field(default_factory=set) # PyCharm сошел с ума, тут все норм


class DBContextManagerTemplate:
    def __init__(self):
        self._db = get_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()


class DBTemplate(DBContextManagerTemplate):
    def __init__(self, model_class: Type[Base], schema_class: Type[BaseModel], params: DBParams = DBParams()):
        super().__init__()
        self._model = model_class
        self._schema = schema_class
        self._params = params

    def create(self, obj: BaseModel) -> None:
        model = self._model(**obj.model_dump(exclude=self._params.exclude_fields_on_creation))
        self._db.add(model)
        self._db.commit()

    def get_obj_by_id(self, obj_id: int) -> Optional[BaseModel]:
        obj = self._db.query(self._model).filter(self._model.id == obj_id).first()
        return self._schema.model_validate(obj, from_attributes=True) if obj else None

    def get_all(self, skip: int = 0, limit: int = 10) -> List[BaseModel]:
        objs = self._db.query(self._model).offset(skip).limit(limit).all()
        return [self._schema.model_validate(obj, from_attributes=True) for obj in objs]

    def update(self, obj_id: int, obj_data: dict) -> Optional[BaseModel]:
        obj = self._db.query(self._model).filter(self._model.id == obj_id).first()
        if obj:
            for key, value in obj_data.items():
                setattr(obj, key, value)
            self._db.commit()
            return self._schema.model_validate(obj, from_attributes=True)
        return None

    def delete(self, obj_id: int) -> Optional[BaseModel]:
        obj = self._db.query(self._model).filter(self._model.id == obj_id).first()
        if obj:
            self._db.delete(obj)
            self._db.commit()
            return self._schema.model_validate(obj, from_attributes=True)
        return None

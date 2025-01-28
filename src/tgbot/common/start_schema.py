from pydantic import BaseModel


class StartSchema(BaseModel):
    wish_list_id: int

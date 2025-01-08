from pydantic import BaseModel


class StartSchema(BaseModel):
    from_user: int

from typing import TypeVar

from pydantic import BaseModel

MessageSchema = TypeVar('MessageSchema', bound=BaseModel)

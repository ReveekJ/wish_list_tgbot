from pydantic import BaseModel, field_validator

from src.services.security_code_manager.security_code_type import SecurityCode


class StartSchema(BaseModel):
    wlId: int
    sc: SecurityCode

    @field_validator('sc', mode='before')
    @classmethod
    def sc_validator(cls, v):
        if isinstance(v, SecurityCode):
            return v
        elif isinstance(v, str):
            return SecurityCode(v)

    class Config:
        arbitrary_types_allowed = True

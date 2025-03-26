import json
import redis

from src.config import REDIS_HOST, REDIS_PORT, REDIS_SECURITY_CODE_DB
from src.services.security_code_manager.security_code_type import SecurityCode


class SecurityCodeManager:
    def __init__(self):
        self.__redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_SECURITY_CODE_DB)

    @staticmethod
    def __key_generator(wish_list_id: int):
        return f'{wish_list_id}'

    def get_security_code(self, wish_list_id: int) -> SecurityCode:
        code = self.__redis.get(self.__key_generator(wish_list_id))
        if code is None:
            return self.update_security_code(wish_list_id)
        return SecurityCode(json.loads(code))

    def update_security_code(self, wish_list_id: int) -> SecurityCode:
        security_code = SecurityCode()
        self.__redis.set(self.__key_generator(wish_list_id), json.dumps(security_code))
        return security_code

    def check_security_code(self, security_code: SecurityCode, wish_list_id: int) -> bool:
        return security_code == self.get_security_code(wish_list_id)

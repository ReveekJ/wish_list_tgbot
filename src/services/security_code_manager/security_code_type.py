import random
import string


class SecurityCode(str):
    def __new__(cls, *args, **kwargs):
        if len(args) != 0:
            return super(SecurityCode, cls).__new__(cls, args[0])
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return super(SecurityCode, cls).__new__(cls, random_string)

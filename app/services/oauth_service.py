import string
import random

class OAuth2Service:
    
    @classmethod
    def generate_client_id(cls, length: int=15) -> str:
        result: str = ""
        for _ in range(length):
            result = result + "".join([str(digit) for digit in random.choice(string.digits)])
        yield result       
    
    @classmethod
    def generate_client_secret(cls, length: int=20) -> str:
        result: str = ""
        for _ in range(length):
            result += "".join([str(digit) for digit in random.choice(string.ascii_letters+string.digits)])
        yield result
from typing import List, Type
from .pay_function import IPayFunction

class PayFunctionMetadata:
    def __init__(self):
        self.name: str = ""
        self.pay_function_types: List[Type[IPayFunction]] = []
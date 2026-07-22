from abc import ABC
from dataclasses import dataclass
from typing import Literal

@dataclass
class Token(ABC):
    """
    Base class for a token
    """

def dummy_function(*args):
    """
    Placeholder for function implementations
    """
    pass

# List of acceptable function names, and map them to actual implementation
# unimplemented functions map to the dummy function
FN_NAME_TO_IMPL_MAP = {
    # arithmetic
    "+": dummy_function,
    "-": dummy_function,
    "*": dummy_function,
    "/": dummy_function,
    "expt": dummy_function,
    "mod": dummy_function,
    # logic
    "and": dummy_function,
    "or": dummy_function,
    "not": dummy_function,
    # list
    "list": dummy_function,
    "first": dummy_function,
    "last": dummy_function
}

class StartParentesisToken(Token):
    def __str__(self) -> str:
        return "("

    def __repr__(self) -> str:
        return "StartParentesisToken"

class EndParentesisToken(Token):
    def __str__(self) -> str:
        return ")"

    def __repr__(self) -> str:
        return "EndParentesisToken"

class FunctionToken(Token):
    """
    Token class for functions
    """
    name: str

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def is_valid(s: str) -> bool:
        """
        Check if the name is a valid function name
        """
        return s in FN_NAME_TO_IMPL_MAP

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"FunctionToken({self.name})"

class ValueToken(Token):
    """
    Token class for values. Only int, float, string, bool are supported.
    """
    value: int | float | str | bool
    type: Literal["int", "float", "str", "bool"]

    def __init__(self, value: int | float | str | bool, type: Literal["int", "float", "str", "bool"]):
        self.value = value
        self.type = type

    @classmethod
    def from_string(cls, s: str):
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            # string
            return cls(value=s[1:-1], type="str")
        elif s == "t":
            # bool
            return cls(value=True, type="bool")
        elif s == "nil":
            return cls(value=False, type="bool")
        elif '.' in s:
            # float
            return cls(value=float(s), type="float")
        else:
            return cls(value=int(s), type="int")

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"ValueToken({self.type}, {str(self.value)})"

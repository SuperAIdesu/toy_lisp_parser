import pprint
from dataclasses import dataclass

from tokens import (
    EndParentesisToken,
    FunctionToken,
    StartParentesisToken,
    Token,
    ValueToken,
)


@dataclass
class AST:
    tokens: list[Token | AST]

    @staticmethod
    def tokenize(s: str) -> list[Token]:
        str_tokens = s.strip().replace("(", " ( ").replace(")", " ) ").split()
        res = []
        for s_tk in str_tokens:
            if s_tk == "(":
                res.append(StartParentesisToken())
            elif s_tk == ")":
                res.append(EndParentesisToken())
            elif FunctionToken.is_valid(s_tk):
                res.append(FunctionToken(name=s_tk))
            else:
                res.append(ValueToken.from_string(s_tk))
        return res

    @classmethod
    def build(cls, s: str):
        tokens = cls.tokenize(s)
        stack = []
        for token in tokens:
            if isinstance(token, EndParentesisToken):
                child_list = []
                while stack and not isinstance(stack[-1], StartParentesisToken):
                    child_list.append(stack.pop())
                stack.pop()
                child_list.reverse()
                stack.append(AST(child_list))
            else:
                stack.append(token)
        return AST(stack)


def interpret(ast: AST | Token):
    if isinstance(ast, Token):
        assert isinstance(ast, ValueToken)
        return ast.value

    tokens = ast.tokens
    if len(tokens) == 1 and isinstance(tokens[0], AST):
        return interpret(tokens[0])
    assert isinstance(tokens[0], FunctionToken)
    fn_token = tokens[0]
    return fn_token.eval(*[interpret(t) for t in tokens[1:]])


if __name__ == "__main__":
    # code = '(first (list "hello" (+ 2.1 3) nil))'
    code = "(* -1 (+ 1 2))"
    ast = AST.build(code)
    pprint.pp(ast)
    result = interpret(ast)
    print(result)

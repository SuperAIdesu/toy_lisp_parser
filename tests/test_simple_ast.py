import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from simple_ast import AST
from tokens import (
    Token,
    ValueToken,
    FunctionToken,
    StartParentesisToken,
    EndParentesisToken,
)


class TestASTTokenize:
    def test_empty_string(self):
        assert AST.tokenize("") == []

    def test_whitespace_only(self):
        assert AST.tokenize("   ") == []

    def test_single_start_paren(self):
        tokens = AST.tokenize("(")
        assert len(tokens) == 1
        assert isinstance(tokens[0], StartParentesisToken)

    def test_single_end_paren(self):
        tokens = AST.tokenize(")")
        assert len(tokens) == 1
        assert isinstance(tokens[0], EndParentesisToken)

    def test_single_integer(self):
        tokens = AST.tokenize("42")
        assert len(tokens) == 1
        assert isinstance(tokens[0], ValueToken)
        assert tokens[0].value == 42

    def test_single_function(self):
        tokens = AST.tokenize("+")
        assert len(tokens) == 1
        assert isinstance(tokens[0], FunctionToken)
        assert tokens[0].name == "+"

    def test_simple_expression(self):
        tokens = AST.tokenize("(+ 1 2)")
        assert len(tokens) == 5
        assert isinstance(tokens[0], StartParentesisToken)
        assert isinstance(tokens[1], FunctionToken)
        assert tokens[1].name == "+"
        assert isinstance(tokens[2], ValueToken)
        assert tokens[2].value == 1
        assert isinstance(tokens[3], ValueToken)
        assert tokens[3].value == 2
        assert isinstance(tokens[4], EndParentesisToken)

    def test_expression_with_float(self):
        tokens = AST.tokenize("(+ 1.5 2.5)")
        value_tokens = [t for t in tokens if isinstance(t, ValueToken)]
        assert value_tokens[0].value == 1.5
        assert value_tokens[1].value == 2.5

    def test_expression_with_string(self):
        tokens = AST.tokenize('(first "hello")')
        value_tokens = [t for t in tokens if isinstance(t, ValueToken)]
        assert value_tokens[0].value == "hello"
        assert value_tokens[0].type == "str"

    def test_expression_with_bool(self):
        tokens = AST.tokenize("(and t nil)")
        value_tokens = [t for t in tokens if isinstance(t, ValueToken)]
        assert value_tokens[0].value is True
        assert value_tokens[1].value is False

    def test_nested_expression(self):
        tokens = AST.tokenize("(+ 1 (* 2 3))")
        fn_tokens = [t for t in tokens if isinstance(t, FunctionToken)]
        assert len(fn_tokens) == 2
        assert fn_tokens[0].name == "+"
        assert fn_tokens[1].name == "*"

    def test_multiple_spaces(self):
        tokens = AST.tokenize("(  +   1   2  )")
        assert len(tokens) == 5

    def test_leading_trailing_whitespace(self):
        tokens = AST.tokenize("  (+ 1 2)  ")
        assert len(tokens) == 5


class TestASTBuild:
    def test_simple_addition(self):
        ast = AST.build("(+ 1 2)")
        assert len(ast.tokens) == 1
        inner = ast.tokens[0]
        assert isinstance(inner, AST)
        assert len(inner.tokens) == 3
        assert isinstance(inner.tokens[0], FunctionToken)
        assert inner.tokens[0].name == "+"
        assert isinstance(inner.tokens[1], ValueToken)
        assert inner.tokens[1].value == 1
        assert isinstance(inner.tokens[2], ValueToken)
        assert inner.tokens[2].value == 2

    def test_nested_expression(self):
        ast = AST.build("(first (list 1 (+ 2 3) 9))")
        assert len(ast.tokens) == 1
        outer = ast.tokens[0]
        assert isinstance(outer, AST)
        assert len(outer.tokens) == 2
        assert isinstance(outer.tokens[0], FunctionToken)
        assert outer.tokens[0].name == "first"

    def test_deeply_nested(self):
        ast = AST.build("(+ (+ 1 2) (+ 3 4))")
        outer = ast.tokens[0]
        assert len(outer.tokens) == 3
        assert outer.tokens[0].name == "+"
        assert isinstance(outer.tokens[1], AST)
        assert isinstance(outer.tokens[2], AST)

    def test_single_value(self):
        ast = AST.build("42")
        assert len(ast.tokens) == 1
        assert isinstance(ast.tokens[0], ValueToken)
        assert ast.tokens[0].value == 42

    def test_multiple_top_level_expressions(self):
        ast = AST.build("(+ 1 2) (+ 3 4)")
        assert len(ast.tokens) == 2
        assert isinstance(ast.tokens[0], AST)
        assert isinstance(ast.tokens[1], AST)

    def test_empty_parens(self):
        ast = AST.build("()")
        assert len(ast.tokens) == 1
        inner = ast.tokens[0]
        assert isinstance(inner, AST)
        assert len(inner.tokens) == 0

    def test_string_value_in_expression(self):
        ast = AST.build('(list "a" "b" "c")')
        inner = ast.tokens[0]
        value_tokens = [t for t in inner.tokens if isinstance(t, ValueToken)]
        assert len(value_tokens) == 3
        assert value_tokens[0].value == "a"
        assert value_tokens[1].value == "b"
        assert value_tokens[2].value == "c"

    def test_bool_values(self):
        ast = AST.build("(and t nil)")
        inner = ast.tokens[0]
        value_tokens = [t for t in inner.tokens if isinstance(t, ValueToken)]
        assert value_tokens[0].value is True
        assert value_tokens[1].value is False

    def test_mixed_types(self):
        ast = AST.build("(list 1 2.5 \"hello\" t nil)")
        inner = ast.tokens[0]
        value_tokens = [t for t in inner.tokens if isinstance(t, ValueToken)]
        assert len(value_tokens) == 5
        assert value_tokens[0].type == "int"
        assert value_tokens[1].type == "float"
        assert value_tokens[2].type == "str"
        assert value_tokens[3].type == "bool"
        assert value_tokens[4].type == "bool"

    def test_expt_function(self):
        ast = AST.build("(expt 2 10)")
        inner = ast.tokens[0]
        assert inner.tokens[0].name == "expt"

    def test_mod_function(self):
        ast = AST.build("(mod 10 3)")
        inner = ast.tokens[0]
        assert inner.tokens[0].name == "mod"

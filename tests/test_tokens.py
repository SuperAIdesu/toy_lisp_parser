import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tokens import (
    Token,
    StartParentesisToken,
    EndParentesisToken,
    FunctionToken,
    ValueToken,
    FN_NAME_TO_IMPL_MAP,
)


class TestStartParentesisToken:
    def test_str(self):
        assert str(StartParentesisToken()) == "("

    def test_repr(self):
        assert repr(StartParentesisToken()) == "StartParentesisToken"

    def test_is_instance_of_token(self):
        assert isinstance(StartParentesisToken(), Token)


class TestEndParentesisToken:
    def test_str(self):
        assert str(EndParentesisToken()) == ")"

    def test_repr(self):
        assert repr(EndParentesisToken()) == "EndParentesisToken"

    def test_is_instance_of_token(self):
        assert isinstance(EndParentesisToken(), Token)


class TestFunctionToken:
    def test_creation(self):
        tok = FunctionToken("+")
        assert tok.name == "+"

    def test_str(self):
        assert str(FunctionToken("mod")) == "mod"

    def test_repr(self):
        assert repr(FunctionToken("+")) == "FunctionToken(+)"

    def test_is_valid_arithmetic(self):
        for name in ["+", "-", "*", "/", "expt", "mod"]:
            assert FunctionToken.is_valid(name) is True

    def test_is_valid_logic(self):
        for name in ["and", "or", "not"]:
            assert FunctionToken.is_valid(name) is True

    def test_is_valid_list(self):
        for name in ["list", "first", "last"]:
            assert FunctionToken.is_valid(name) is True

    def test_is_valid_unknown(self):
        assert FunctionToken.is_valid("unknown_func") is False

    def test_is_valid_empty_string(self):
        assert FunctionToken.is_valid("") is False

    def test_is_instance_of_token(self):
        assert isinstance(FunctionToken("+"), Token)


class TestValueToken:
    def test_int_creation(self):
        tok = ValueToken(42, "int")
        assert tok.value == 42
        assert tok.type == "int"

    def test_float_creation(self):
        tok = ValueToken(3.14, "float")
        assert tok.value == 3.14
        assert tok.type == "float"

    def test_str_creation(self):
        tok = ValueToken("hello", "str")
        assert tok.value == "hello"
        assert tok.type == "str"

    def test_bool_true_creation(self):
        tok = ValueToken(True, "bool")
        assert tok.value is True
        assert tok.type == "bool"

    def test_bool_false_creation(self):
        tok = ValueToken(False, "bool")
        assert tok.value is False
        assert tok.type == "bool"

    def test_int_str(self):
        assert str(ValueToken(42, "int")) == "42"

    def test_float_str(self):
        assert str(ValueToken(3.14, "float")) == "3.14"

    def test_str_str(self):
        assert str(ValueToken("hello", "str")) == "hello"

    def test_bool_str(self):
        assert str(ValueToken(True, "bool")) == "True"

    def test_int_repr(self):
        assert repr(ValueToken(42, "int")) == "ValueToken(int, 42)"

    def test_str_repr(self):
        assert repr(ValueToken("hello", "str")) == "ValueToken(str, hello)"

    def test_is_instance_of_token(self):
        assert isinstance(ValueToken(1, "int"), Token)


class TestValueTokenFromString:
    def test_parse_quoted_string(self):
        tok = ValueToken.from_string('"hello"')
        assert tok.value == "hello"
        assert tok.type == "str"

    def test_parse_empty_quoted_string(self):
        tok = ValueToken.from_string('""')
        assert tok.value == ""
        assert tok.type == "str"

    def test_parse_bool_true(self):
        tok = ValueToken.from_string("t")
        assert tok.value is True
        assert tok.type == "bool"

    def test_parse_bool_nil(self):
        tok = ValueToken.from_string("nil")
        assert tok.value is False
        assert tok.type == "bool"

    def test_parse_positive_float(self):
        tok = ValueToken.from_string("3.14")
        assert tok.value == 3.14
        assert tok.type == "float"

    def test_parse_negative_float(self):
        tok = ValueToken.from_string("-2.5")
        assert tok.value == -2.5
        assert tok.type == "float"

    def test_parse_positive_int(self):
        tok = ValueToken.from_string("42")
        assert tok.value == 42
        assert tok.type == "int"

    def test_parse_negative_int(self):
        tok = ValueToken.from_string("-10")
        assert tok.value == -10
        assert tok.type == "int"

    def test_parse_zero(self):
        tok = ValueToken.from_string("0")
        assert tok.value == 0
        assert tok.type == "int"

    def test_parse_zero_float(self):
        tok = ValueToken.from_string("0.0")
        assert tok.value == 0.0
        assert tok.type == "float"


class TestFNNameToImplMap:
    def test_contains_arithmetic_ops(self):
        for op in ["+", "-", "*", "/", "expt", "mod"]:
            assert op in FN_NAME_TO_IMPL_MAP

    def test_contains_logic_ops(self):
        for op in ["and", "or", "not"]:
            assert op in FN_NAME_TO_IMPL_MAP

    def test_contains_list_ops(self):
        for op in ["list", "first", "last"]:
            assert op in FN_NAME_TO_IMPL_MAP

    def test_all_values_callable(self):
        for impl in FN_NAME_TO_IMPL_MAP.values():
            assert callable(impl)

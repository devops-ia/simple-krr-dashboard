"""Tests for the utility functions."""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from simple_krr_dashboard.components.table import (
    convert_to_camel_case,
    format_integer,
    format_status_badge,
    read_csv_file,
)


def test_convert_to_camel_case():
    """Test conversion from snake_case to camelCase."""
    assert convert_to_camel_case("hello_world") == "helloWorld"
    assert convert_to_camel_case("test_case_string") == "testCaseString"
    assert convert_to_camel_case("single") == "single"
    assert convert_to_camel_case("") == ""


def test_format_integer():
    """Test integer formatting."""
    assert format_integer(1000) == "1000"
    assert format_integer(1000000) == "1000000"
    assert format_integer(0) == "0"
    assert format_integer("1000") == "1000"
    assert format_integer(None) == ""

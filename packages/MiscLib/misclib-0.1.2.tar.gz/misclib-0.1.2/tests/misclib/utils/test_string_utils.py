from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from misclib.utils.string import (
    camel_case,
    kebab_case,
    normalize_str,
    pascal_case,
    snake_case,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    ('input_str', 'expected'),
    [
        ('test_camel_case', 'testCamelCase'),
        ('test-camel-case', 'testCamelCase'),
        ('test-Camel_case', 'testCamelCase'),
        ('TEST_CAMEL_CASE', 'testCamelCase'),
        ('TestCamelCase', 'testCamelCase'),
        ('testCamelCase', 'testCamelCase'),
    ],
)
def test_camel_case(input_str: str, expected: str) -> None:
    assert camel_case(input_str) == expected


@pytest.mark.parametrize(
    ('input_str', 'expected'),
    [
        ('testSnakeCase', 'test_snake_case'),
        ('TestSnakeCase', 'test_snake_case'),
        ('test-Snake_case', 'test_snake_case'),
        ('TEST_SNAKE_CASE', 'test_snake_case'),
        ('test-snake-case', 'test_snake_case'),
        ('test_snake_case', 'test_snake_case'),
    ],
)
def test_snake_case(input_str: str, expected: str) -> None:
    assert snake_case(input_str) == expected


@pytest.mark.parametrize(
    ('input_str', 'expected'),
    [
        ('test_pascal_case', 'TestPascalCase'),
        ('test-pascal-case', 'TestPascalCase'),
        ('test-Pascal_case', 'TestPascalCase'),
        ('TEST_PASCAL_CASE', 'TestPascalCase'),
        ('testPascalCase', 'TestPascalCase'),
        ('TestPascalCase', 'TestPascalCase'),
    ],
)
def test_pascal_case(input_str: str, expected: str) -> None:
    assert pascal_case(input_str) == expected


@pytest.mark.parametrize(
    ('input_str', 'expected'),
    [
        ('TestKebabCase', 'test-kebab-case'),
        ('testKebabCase', 'test-kebab-case'),
        ('test-Kebab_case', 'test-kebab-case'),
        ('TEST_KEBAB_CASE', 'test-kebab-case'),
        ('test_kebab_case', 'test-kebab-case'),
        ('test-kebab-case', 'test-kebab-case'),
    ],
)
def test_kebab_case(input_str: str, expected: str) -> None:
    assert kebab_case(input_str) == expected


@pytest.mark.parametrize(
    ('input_str', 'expected_result'),
    [
        pytest.param('a' * 10**6, 'a' * 10**6, id='long_lowercase'),  # (no matches).
        pytest.param('A' * 10**6, 'a' * 10**6, id='long_uppercase'),  # (no matches).
        pytest.param('1' * 10**6 + 'A', '1' * 10**6 + '_a', id='digits_and_uppercase'),
    ],
)
def test_regex_pattern_correctness(
    regex_pattern_runner: Callable[[str], tuple[str, float]],
    input_str: str,
    expected_result: str,
) -> None:
    result, _ = regex_pattern_runner(input_str)
    assert result == expected_result


@pytest.mark.parametrize(
    'input_str',
    [
        pytest.param('a' * 10**6, id='long_lowercase'),
        pytest.param('A' * 10**6, id='long_uppercase'),
        pytest.param('aA' * 5 * 10**5, id='alternating_case'),
        pytest.param('1' * 10**6 + 'A', id='digits_followed_by_uppercase'),
        pytest.param('a' + 'B' * 10**5 + 'a' + 'B' * 10**5, id='large_blocks_uppercase'),
        pytest.param('a' * 10**5 + 'Z' * 10**5 + 'a' * 10**5, id='mixed_long_sequences'),
    ],
)
def test_regex_pattern_performance(
    regex_pattern_runner: Callable[[str], tuple[str, float]],
    input_str: str,
) -> None:
    _, execution_time = regex_pattern_runner(input_str)
    msg = f'Execution time ({execution_time:.6f} seconds) '
    msg += f'exceeded 1 second for input length {len(input_str)}'
    assert execution_time < 1.0, msg


@pytest.mark.parametrize(
    ('input_value', 'expected'),
    [
        # Single string with whitespace.
        ('  TestString  ', 'teststring'),
        # List with duplicates.
        (['  TestString  ', 'teststring', 'TESTSTRING', 'TeStStRiNg'], 'teststring'),
        # List with case differences.
        (['apple', 'Banana', 'banana', 'APPLE'], ['apple', 'banana']),
        ('', ''),  # Empty string.
        ([], []),  # Empty list.
        (['  '], ''),  # List with whitespace-only string.
    ],
)
def test_normalize_str(input_value: list[str] | str, expected: list[str] | str) -> None:
    assert normalize_str(input_value) == expected

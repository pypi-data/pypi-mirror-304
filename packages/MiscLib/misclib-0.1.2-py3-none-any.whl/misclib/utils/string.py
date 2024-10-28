from __future__ import annotations

import re

from misclib.constants import CAMEL_TO_SNAKE_RE


def camel_case(v: str, /) -> str:
    """Convert a string to camelCase."""
    v = v.replace('-', '_')
    parts = v.split('_')
    if len(parts) > 1:
        v = ''.join(part.title() for part in parts)
    return v[0].lower() + v[1:]


def snake_case(v: str, /) -> str:
    """Convert a string to snake_case."""
    v = v.replace('-', '_')
    v = re.sub(CAMEL_TO_SNAKE_RE, r'_\1', v)
    return v.lower()


def pascal_case(v: str, /) -> str:
    """Convert a string to PascalCase."""
    camelcase_str = camel_case(v)
    return camelcase_str[0].upper() + camelcase_str[1:]


def kebab_case(v: str, /) -> str:
    """Convert a string to kebab-case."""
    v = v.replace('_', '-')
    v = re.sub(CAMEL_TO_SNAKE_RE, r'-\1', v)
    return v.lower()


def normalize_str(v: list[str] | str, /) -> list[str] | str:
    """Normalize one or more string values (i.e., for use in comparisons) by stripping them of
    whitespace, casefolding, deduplicating, and sorting them in ascending lexicographic order.

    Parameters
    ----------
    v : list[str] | str
        A string or list of strings to be normalized.

    Returns
    -------
    list[str] | str
        The normalized string(s). If given input of multiple strings and only a single
        string remains, it will be returned as a `str` rather than a `list[str]`.
    """
    v = [v] if isinstance(v, str) else v
    v_set = sorted({str(item).strip().casefold() for item in v})
    if len(v_set) == 1:
        return next(iter(v_set))
    return v_set

import json
import re
import time
from collections.abc import Callable
from pathlib import Path

import pytest

from misclib.constants import CAMEL_TO_SNAKE_RE

_test_data: Path = Path(__file__).resolve().parent / 'data'


@pytest.fixture
def regex_pattern_runner() -> Callable[[str], tuple[str, float]]:
    """Fixture that provides a function to test regex pattern performance and results.

    Returns
    -------
    Callable[[str], tuple[str, float]]
        Callable that takes a string input and returns a tuple of (result, execution_time).
    """

    def _run(input_str: str) -> tuple[str, float]:
        start_time = time.time()
        result = re.sub(CAMEL_TO_SNAKE_RE, r'_\1', input_str).lower()
        end_time = time.time()
        return result, end_time - start_time

    return _run


@pytest.fixture
def chunk(request: pytest.FixtureRequest) -> list[tuple[str, bool]]:
    """Fixture that provides chunks of test data for venv path testing.

    Returns
    -------
    list[tuple[str, bool]]
        A chunk of test data containing tuples of (path, is_venv_path).
    """
    if (
        not (_venv_paths_json := (_test_data / 'venv_paths.json')).exists()
        or not (_non_venv_paths_json := (_test_data / 'non_venv_paths.json')).exists()
    ):
        raise FileNotFoundError(
            f'Unable to locate one or more JSON files required for testing:\n'
            f"\t'{_test_data}/venv_paths.json'\n"
            f'and/or\n'
            f"\t'{_test_data}/non_venv_paths.json'\n"
            'appear to be missing.'
        )

    with _venv_paths_json.open() as _venv_paths, _non_venv_paths_json.open() as _non_venv_paths:
        venv_paths = json.load(_venv_paths)
        non_venv_paths = json.load(_non_venv_paths)

    chunk_size = 100
    test_data = [(path, True) for path in venv_paths] + [(path, False) for path in non_venv_paths]
    chunks = [test_data[i : i + chunk_size] for i in range(0, len(test_data), chunk_size)]
    return chunks[0] if not hasattr(request, 'param') else chunks[request.param]

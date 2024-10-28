from __future__ import annotations

import os
from pathlib import Path

import pytest

from misclib.utils.path import (
    dir_path_from_env,
    file_path_from_env,
    is_venv,
    mkdir,
    mkfile,
    resolve_path,
)


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def test_resolve_path_file_exists(temp_dir: Path) -> None:
    test_file = temp_dir / 'test_file'
    test_file.touch()

    result = resolve_path(str(test_file))
    assert result == test_file.resolve()


def test_resolve_path_dir_exists(temp_dir: Path) -> None:
    result = resolve_path(str(temp_dir))
    assert result == temp_dir.resolve()


def test_resolve_path_nonexist_not_strict() -> None:
    non_existent_path = '/path/to/nonexist'
    result = resolve_path(non_existent_path, strict=False)
    assert result is not None
    assert isinstance(result, Path)


def test_resolve_path_nonexist_strict() -> None:
    non_existent_path = '/path/to/nonexist'
    result = resolve_path(non_existent_path, strict=True)
    assert result is None


def test_resolve_path_tilde() -> None:
    result = resolve_path('~')
    assert result == Path.home()


def test_resolve_path_home_var() -> None:
    result = resolve_path('$HOME')
    assert result == Path.home()


def test_resolve_path_relative(temp_dir: Path) -> None:
    os.chdir(temp_dir)
    relative_path = './relative_dir'
    Path(relative_path).mkdir(exist_ok=True, parents=True)

    result = resolve_path(relative_path)
    assert result == (temp_dir / relative_path).resolve()


def test_resolve_path_symlink(temp_dir: Path) -> None:
    original_dir = temp_dir / 'original_dir'
    original_dir.mkdir()
    symlink_dir = temp_dir / 'symlink_dir'
    os.symlink(original_dir, symlink_dir)

    result = resolve_path(str(symlink_dir))
    assert result == original_dir.resolve()


def test_resolve_path_absolute(temp_dir: Path) -> None:
    os.chdir(temp_dir)
    absolute_path = Path.cwd() / 'absolute'
    absolute_path.touch()
    absolute_path = absolute_path.absolute()

    result = resolve_path(str(absolute_path))
    assert result == absolute_path


def test_mkdir(temp_dir: Path) -> None:
    dir_path = temp_dir / 'new_dir'
    result = mkdir(dir_path)

    assert result == dir_path.resolve()
    assert dir_path.exists()
    assert dir_path.is_dir()


def test_mkfile(temp_dir: Path) -> None:
    file_path = temp_dir / 'new_file.txt'
    result = mkfile(file_path)

    assert result == file_path.resolve()
    assert file_path.exists()
    assert file_path.is_file()


def test_file_path_from_env(
    monkeypatch: pytest.MonkeyPatch,
    temp_dir: Path,
) -> None:
    file_path = temp_dir / 'test_file'
    monkeypatch.setenv('TEST_FILE_PATH', str(file_path))
    result = file_path_from_env('TEST_FILE_PATH')

    assert result == file_path.resolve()
    assert file_path.exists()
    assert file_path.is_file()


def test_dir_path_from_env(
    monkeypatch: pytest.MonkeyPatch,
    temp_dir: Path,
) -> None:
    dir_path = temp_dir / 'test_dir'
    monkeypatch.setenv('TEST_DIR_PATH', str(dir_path))
    result = dir_path_from_env('TEST_DIR_PATH')

    assert result == dir_path.resolve()
    assert dir_path.exists()
    assert dir_path.is_dir()


def test_no_resolve_links(
    monkeypatch: pytest.MonkeyPatch,
    temp_dir: Path,
) -> None:
    dir_path = temp_dir / 'test_dir'
    monkeypatch.setenv('TEST_DIR_PATH', str(dir_path))
    result = dir_path_from_env('TEST_DIR_PATH')

    assert result == dir_path.resolve()
    assert dir_path.exists()
    assert dir_path.is_dir()


@pytest.mark.parametrize('chunk', range(20), indirect=['chunk'])
def test_is_venv(chunk: list[tuple[str, bool]]) -> None:
    """Test `is_venv` function with `str` paths."""
    for path, expected in chunk:
        assert is_venv(path) == expected


@pytest.mark.parametrize('chunk', range(20), indirect=['chunk'])
def test_is_venv_with_pathlib(chunk: list[tuple[str, bool]]) -> None:
    """Test `is_venv` function with `Path` object paths."""
    for path, expected in chunk:
        assert is_venv(Path(path)) == expected

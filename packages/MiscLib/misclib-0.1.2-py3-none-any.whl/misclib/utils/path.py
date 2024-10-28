from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from misclib.constants import VIRTUALENV_RE

load_dotenv()


def _expand_path(path: str | Path, *, resolve: bool = False, strict: bool = False) -> Path:
    # This is totally non-intuitive but:
    #    path.Home() != Path('$HOME').expanduser()
    # Evidently, Path.expanduser() only expands '~' and not '$HOME'
    expanded = Path(os.path.expandvars(str(path))).expanduser()
    return expanded.resolve(strict=strict) if resolve else expanded


def resolve_path(path: str | Path, *, strict: bool = False) -> Path | None:
    """Return the resolved `Path` object of a specified file
    or directory path, or `None` if any error occurs."""
    try:
        return _expand_path(path, resolve=True, strict=strict)
    except Exception:
        return None


def is_venv(path: str | Path, /) -> bool:
    """Return `True` or `False` whether the specified path value exists
    within a site-packages or other Python VirtualEnv directory path."""
    return VIRTUALENV_RE.search(str(path)) is not None


def mkfile(
    file_path: str | Path,
    *,
    file_mode: int = 0o0600,
    dir_mode: int = 0o0700,
    resolve: bool = True,
) -> Path:
    """Create a file and its parent directories if they don't exist.

    Parameters
    ----------
    file_path : str | Path
        The path to the file to be created.
    file_mode : int, optional
        The file mode (permissions) to set for the created file,
        by default 0o0600.
    dir_mode : int, optional
        The directory mode (permissions) to set for created parent directories,
        by default 0o0700.
    resolve : bool, optional
        Whether to resolve the path, by default True.

    Returns
    -------
    Path
        The path to the created file, resolved if `resolve` is True.
    """

    path = _expand_path(file_path)
    if not path.exists():
        if not path.parent.exists():
            path.parent.mkdir(mode=dir_mode, parents=True, exist_ok=True)
        path.touch(mode=file_mode, exist_ok=True)
    return path.resolve() if resolve else path


def mkdir(
    dir_path: str | Path,
    *,
    dir_mode: int = 0o0700,
    resolve: bool = True,
) -> Path:
    """Create a directory and its parent directories if they don't exist.

    Parameters
    ----------
    dir_path : str | Path
        The path to the directory to be created.
    dir_mode : int, optional
        The directory mode (permissions) to set for created directories,
        by default 0o0700.
    resolve : bool, optional
        Whether to resolve the path, by default True.

    Returns
    -------
    Path
        The path to the created directory, resolved if `resolve` is True.
    """

    path = _expand_path(dir_path)
    if not path.exists():
        path.mkdir(mode=dir_mode, parents=True, exist_ok=True)
    return path.resolve() if resolve else path


def dir_path_from_env(
    var: str,
    *,
    dir_mode: int = 0o0700,
    ensure_exists: bool = True,
    resolve: bool = True,
) -> Path | None:
    """Get a directory path from an environment variable and optionally create it.

    Parameters
    ----------
    var : str
        The name of the environment variable containing the directory path.
    dir_mode : int, optional
        The directory mode (permissions) to set if creating the directory,
        by default 0o0700.
    ensure_exists : bool, optional
        Whether to create the directory if it doesn't exist, by default True.
    resolve : bool, optional
        Whether to resolve the path, by default True.

    Returns
    -------
    Path | None
        The path to the directory, or None if the environment variable is not set.
    """

    if (str_path := os.getenv(var)) is not None:
        path = _expand_path(str_path)
        if ensure_exists and not path.exists():
            path.mkdir(mode=dir_mode, parents=True, exist_ok=True)
        return path.resolve() if resolve else path
    return None


def file_path_from_env(
    var: str,
    *,
    file_mode: int = 0o0600,
    dir_mode: int = 0o0700,
    ensure_exists: bool = True,
    resolve: bool = True,
) -> Path | None:
    """Get a file path from an environment variable and optionally create it.

    Parameters
    ----------
    var : str
        The name of the environment variable containing the file path.
    file_mode : int, optional
        The file mode (permissions) to set if creating the file,
        by default 0o0600.
    dir_mode : int, optional
        The directory mode (permissions) to set if creating parent directories,
        by default 0o0700.
    ensure_exists : bool, optional
        Whether to create the file and its parent directories if they don't
        exist, by default True.
    resolve : bool, optional
        Whether to resolve the path, by default True.

    Returns
    -------
    Path | None
        The path to the file, or None if the environment variable is not set.
    """

    if (str_path := os.getenv(var)) is not None:
        path = _expand_path(str_path)
        if ensure_exists and not path.exists():
            if not path.parent.exists():
                path.mkdir(mode=dir_mode, parents=True, exist_ok=True)
            path.touch(mode=file_mode, exist_ok=True)
        return path.resolve() if resolve else path
    return None

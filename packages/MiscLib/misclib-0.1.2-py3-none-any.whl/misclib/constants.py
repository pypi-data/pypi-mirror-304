from __future__ import annotations

import re

CAMEL_TO_SNAKE_RE: re.Pattern[str] = re.compile(r'(?<=[a-z0-9])([A-Z])')

VIRTUALENV_RE: re.Pattern[str] = re.compile(
    r'(^|[\\/])(\.?virtualenv|\.?venv|\.?env|lib[\\/python[0-9]+\.[0-9]+]'
    r'[\\/site-packages])([\\/]|$)'
)

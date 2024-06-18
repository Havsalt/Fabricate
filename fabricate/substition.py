import re as _re
from functools import partial as _partial

from actus import error as _error


_KEY_PATTERN = _re.compile(
    r"\$inject\[(\w+)\]",
    flags=_re.RegexFlag.ASCII
)


def collect_format_keys(
    format_string: str
) -> list[str]:
    return _KEY_PATTERN.findall(format_string)


def _replace_keyword(
    match: _re.Match[str],
    /,
    *,
    pairs: dict[str, str],
    blueprint_name: str
) -> str:
    key = match.group(1)
    if key in pairs:
        return pairs[key]
    _error(f"No value found for $[{key}] in blueprint $[{blueprint_name}]")
    return key


def inject_values(
    string: str,
    /,
    *,
    pairs: dict[str, str],
    blueprint_name: str
) -> str:
    partial_replace_keyword = _partial(
        _replace_keyword,
        pairs=pairs,
        blueprint_name=blueprint_name
    )
    return _KEY_PATTERN.sub(partial_replace_keyword, string)

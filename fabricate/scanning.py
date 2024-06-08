from typing import Generator as _Generator


def collect_format_keys(format_string: str) -> _Generator[str, None, None]:
    remaining = format_string
    dummy_kwargs: dict[str, None] = {}
    while remaining:
        try:
            _formatted = format_string.format(**dummy_kwargs)
        except KeyError as lookup_error:
            for key in lookup_error.args:
                dummy_kwargs.setdefault(key, None)
                yield key
        remaining = remaining[1:]

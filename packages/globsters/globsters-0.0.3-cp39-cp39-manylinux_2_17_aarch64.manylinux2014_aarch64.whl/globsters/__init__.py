from __future__ import annotations
from os import sep
from functools import lru_cache
from typing import Sequence, Union, Tuple

from globsters.libglobsters import Globster as Globster
from globsters.libglobsters import Globsters as Globsters
from globsters.libglobsters import __version_lib__ as __version_lib__
from globsters.libglobsters import bslash2fslash as bslash2fslash
from globsters.libglobsters import fslash2bslash as fslash2bslash

__version__ = __version_lib__
__all__ = ("__version__", "Globster", "Globsters", "globster", "globsters")

_backslash_escape = sep != "\\"


@lru_cache(maxsize=16)
def _globster(
    pattern: Union[Tuple[str, ...], str],
    case_insensitive: bool = False,
    literal_separator: bool = False,
    backslash_escape: bool = _backslash_escape,
) -> Globster:
    return Globsters(
        (pattern,) if isinstance(pattern, str) else pattern,
        case_insensitive,
        literal_separator,
        backslash_escape,
    )


def globster(
    patterns: Union[Sequence[str], str],
    case_insensitive: bool = False,
    literal_separator: bool = False,
    backslash_escape: bool = _backslash_escape,
    cache: bool = True,
) -> Globsters:
    """Create a Globster object from a glob pattern(s)"""
    if cache:
        if isinstance(patterns, str):
            return _globster(
                patterns, case_insensitive, literal_separator, backslash_escape
            )
        return _globster(
            tuple(set(patterns)), case_insensitive, literal_separator, backslash_escape
        )
    if isinstance(patterns, str):
        return globster(
            (patterns,), case_insensitive, literal_separator, backslash_escape, cache
        )
    return Globsters(tuple(set(patterns)), case_insensitive)


def globsters(
    patterns: Sequence[str],
    case_insensitive: bool = False,
    literal_separator: bool = False,
    backslash_escape: bool = _backslash_escape,
    cache: bool = True,
) -> Globsters:
    """Create a Globster object from a glob pattern(s)"""
    if cache:
        return _globster(
            tuple(set(patterns)), case_insensitive, literal_separator, backslash_escape
        )
    return Globsters(
        tuple(set(patterns)), case_insensitive, literal_separator, backslash_escape
    )


__doc__ = globsters.__doc__
if hasattr(globsters, "__all__"):
    __all__ = globsters.__all__

from __future__ import annotations

import pandas as pd
from typing import (
    Optional, 
    TypeVar,
    List, 
    Union,
    overload,
)

T = TypeVar("T")

@overload
def convert_list_arg(
    arg: Union[List[T], T, str], default: Optional[List[T]] = None
) -> str:
    ...

@overload
def convert_list_arg(arg: None=None, default: List[T]=None) -> str:
    ...

@overload
def convert_list_arg(arg: None=None, default: None=None) -> None:
    ...

def convert_list_arg(arg=None, default=None):
    """
    Converts a list of arguments to a comma separated string.
    ---
    The overloading allows endpoints with generic dimension and metric types
    to pass those arguments to this function without type issues.
    """
    if isinstance(arg, list):
        return ",".join([str(x) for x in arg])
    if not arg and default:
        return ",".join([str(x) for x in default])
    if arg is not None:
        return str(arg)
    return arg

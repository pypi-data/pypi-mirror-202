from __future__ import annotations
import re
from singular_client import *
from typing import *

def get_pandas():
    try:
        import pandas as pd
        return pd
    except ImportError:
        raise ImportError(
            "pandas is required to use `singular-client` utility methods. Please `pip install pandas`"
        )


def standardize_name(s: str) -> str:
    """
    Convert a string to column-name friendly snake case.
    Example: " This   (x) is a__str " -> "this_x_is_a__str"
    """
    import re

    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" ?- ?", " ", s)
    s = re.sub(r"[^A-Za-z0-9_ ]+", "", s)
    s = s.replace(" ", "_")
    return s


def name_value_mapping(
    docs: List[NameDocValues],
    dimension_key: Literal["display_name", "name"] = "display_name",
    value_key: Literal["display_name", "name"] = "display_name",
) -> Dict[str, Dict[str, str]]:
    """
    Before:
    [
        {
          "name": "<dimension_name>",
          "display_name": "<dimension_display_name>",
          "values": [
              {"name": "<value_name>", "display_name": "<value_display_name>"},
              {"name": "<value_name>", "display_name": "<value_display_name>"},
            ],
        },
    ]
    After:
    [
      "<dimension_display_name>": {
        "<value_display_name>": "<value_name>",
        "<value_display_name>": "<value_name>",
      },
    ]
    """
    value_value = "name" if value_key == "display_name" else "display_name"
    return {
        doc[dimension_key]: {
            value[value_key]: value[value_value] for value in doc["values"]
        }
        for doc in docs
    }


def name_mapping(
    docs: List[NameDoc],
    key: Literal["display_name", "name"] = "display_name",
) -> Dict[str, str]:
    """
    Before:
    [
        {"name": "<name>", "display_name": "<display_name>"},
        {"name": "<name>", "display_name": "<display_name>"},
    ]
    After:
    [
      "<display_name>": "<name>",
      "<display_name>": "<name>",
    ]
    """
    value = "name" if key == "display_name" else "display_name"
    return {doc[key]: doc[value] for doc in docs}

# INTERNAL UTILITY FUNCTIONS


T = TypeVar("T")


@overload
def _convert_list_arg(
    arg: Union[List[T], T, str], default: Optional[List[T]] = None
) -> str:
    ...


@overload
def _convert_list_arg(arg: None = None, default: List[T] = None) -> str:
    ...


@overload
def _convert_list_arg(arg: None = None, default: None = None) -> None:
    ...


def _convert_list_arg(arg=None, default=None):
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

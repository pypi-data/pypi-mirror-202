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


def pretty_time(t: float) -> str:
    """
    Convert a unix timestamp to a pretty string.
    Example: 1616284202.0 -> "5/21 4:23:22 PM"
    """
    import datetime
    return datetime.datetime.fromtimestamp(t).strftime("%I:%M:%S %p, %m/%d")


def standardize_name(s: str) -> str:
    """
    Convert a string to column-name friendly snake case.
    Example: " This   (x) is a__str " -> "this_x_is_a__str"
    """
    import re

    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" ?- ?", " ", s)
    s = re.sub(r" . ", " ", s)
    s = re.sub(r"[^A-Za-z0-9_ ]+", "", s)
    s = s.replace(" ", "_")
    return s

def format_constant(s: str) -> str:
    """
    replace all "xX" with "X_X" and uppercase the result
    """
    s = standardize_name(s)
    s = re.sub(r"([^A-Z_])([A-Z])", r"\1_\2", s)
    return s.upper()


def format_variable(s: str) -> str:
    """
    replace all "xX" with "x_x" and lowercase the result
    """
    s = standardize_name(s)
    s = re.sub(r"([^a-z_])([A-Z])", r"\1_\2", s)
    return s.lower()


def format_type(s: str) -> str:
    """
    ONE_two_three -> OneTwoThree
    ONE_twoThree -> OneTwoThree
    oneTwo_three -> OneTwoThree
    """
    import re

    def to_title(match):
        return match.group(1).title()

    def to_upper(match):
        return match.group(1).upper()

    s = standardize_name(s)
    # Leading lowercase to title
    s = re.sub(r"^([a-z])", to_upper, s)
    # Uppercase to title
    s = re.sub(r"([A-Z]+)", to_title, s)
    # Underscore title or lowercase to title without underscore
    s = re.sub(r"_([A-Za-z][a-z]+)", to_title, s)
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

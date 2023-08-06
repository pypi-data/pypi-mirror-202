from singular_client.utils import (
    get_custom_fields_unique_flagged,
    get_custom_fields,
    format_type,
    format_constant,
    format_variable,
    read_raw_html,
)
from singular_client import SingularAPI
import pandas as pd, numpy as np

pd.set_option("display.max_rows", None)
pd.set_option("display.min_rows", None)
import re
from typing import *
from singular_client.utils import (
    format_type,
    format_constant,
    format_variable,
    read_raw_html,
)

DEFAULT_PY_MODULE_FILENAME = "custom_fields.py"


def main(
    api: Optional[SingularAPI] = None,
    key: Optional[str] = None,
    module_filename: str = DEFAULT_PY_MODULE_FILENAME,
):
    df = get_custom_fields_unique_flagged(api=api, key=key)
    df["skan_event_and_cohort_metric"] = df["cohort_metric"] & df["skan_event"]
    df["filter_and_custom_dimension"] = df["custom_dimension"] & df["filter"]
    group_cols = [c for c in df if c not in ["display", "column"]]

    def options(sr: pd.Series) -> list:
        return list(set(list(sr)))

    def all_options(df):
        return list(set(options(df.display) + options(df.column)))

    s = DOC + IMPORTS
    base = "custom_field"

    s += generate_spec(base, all_options(df))
    s += generate_spec(base + "_display", options(df.display))
    s += generate_spec(base + "_column", options(df.column))

    for col in group_cols:
        df_filtered = df[df[col]]
        s += generate_spec(col, all_options(df_filtered))
        s += generate_spec(col + "_display", options(df_filtered.display))
        s += generate_spec(col + "_column", options(df_filtered.column))

        mapping = dict(zip(df_filtered.column, df_filtered.display))
        s += gen_field_mapping(col.upper() + "_MAPPING", mapping)

    with open(module_filename, "w") as f:
        f.write(s)
    return s


def list_value(value: str) -> str:
    return f'    "{value}",\n'


def dict_item(key: str, value: str) -> str:
    return f'    "{key}": "{value}",\n'


def literal_type_name(name: str) -> str:
    return format_type(name)


def constant_type_name(name: str) -> str:
    return format_constant(name)


def args_type_name(name: str) -> str:
    return format_type(name + "_args")


def validator_func_name(name: str) -> str:
    return format_variable("is_" + name)


def gen_literal_type(name: str, values: Iterable[str]) -> str:
    """Create Literal type using `values` as args"""
    type_name = literal_type_name(name)
    s = type_name + " = Literal[\n"
    for value in values:
        s += list_value(value)
    return s + "]\n\n"


def gen_args_type(name: str) -> str:
    """
    Create a Union type that allows for an iterable of valid literals
    of a type, or a single string
    """
    type_name = literal_type_name(name)
    args_name = args_type_name(name)
    return f"{args_name} = Union[Iterable[{type_name}], str]\n\n"


def gen_constant_list(name: str) -> str:
    """Extract args from Literal, `name`"""
    type_name = literal_type_name(name)
    const_name = constant_type_name(name)
    return f"{const_name} = list(get_args({type_name}))\n\n"


def gen_validator_func_for_type(name: str) -> str:
    """Create validator function for type `name`"""
    constant_name = constant_type_name(name)
    validator_name = validator_func_name(name)
    type_name = literal_type_name(name)
    return f'''def {validator_name}(name: Union[str, {type_name}]) -> bool:
    """
    Check if `name` is a valid custom `{type_name}` from Singular.
    """
    return name in {constant_name}


'''


def generate_spec(name: str, values: Iterable[str]) -> str:
    """Generate all 4 required items"""
    return (
        # literal_type_name(name) + "\n"
        gen_literal_type(name, values)
        + gen_args_type(name)
        + gen_constant_list(name)
        + gen_validator_func_for_type(name)
    )


def gen_field_mapping(name: str, mapping: dict) -> str:
    """Generate dictionary with field name to display name mapping"""
    s = format_constant(name) + " = {\n"
    for k, v in mapping.items():
        s += dict_item(k, v)
    return s + "}\n\n"


IMPORTS = "from typing import Literal, Iterable, Union, get_args\n\n\n"

DOC = '''"""
VALID CUSTOM FIELD TYPES FOR ENDPOINTS
======================================
"""

'''


if __name__ == "__main__":
    main()

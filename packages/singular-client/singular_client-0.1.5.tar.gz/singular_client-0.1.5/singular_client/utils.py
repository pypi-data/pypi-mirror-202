from __future__ import annotations
import re
import time
from singular_client import *
from typing import *
import pandas as pd
import numpy as np

def get_custom_fields(
    api: Optional[SingularAPI] = None, key: Optional[str] = None
) -> pd.DataFrame:
    """
    Get a DataFrame of all custom fields in the Singular account.
    Endpoints:
        Filters
        Custom Dimensions
        Cohort Metrics
        Conversion Metrics
        SKAN Events
        Apps
        Partners

    Columns:
        kind: str
        id
        display
        id_field: str
        display_field: str
        custom_name: str (custom string extracted from `display`)
    """
    api = api or SingularAPI(key=key)
    import pickle
    with open('test_get_custom.pkl', 'rb') as f:
        return pickle.load(f)

    def call_endpoint(endpoint: str, **kwargs) -> List[Dict[str, Any]]:
        """Calls dynamically by name, delays to avoid rate limit, handles custom cases."""
        res = delay(getattr(api, endpoint).request, seconds=0.2, **kwargs)
        if endpoint == "cohort_metrics":
            # Cohort metrics returns both metrics and periods
            return res["metrics"]
        return res

    # Call all endpoints and parse the id mapping for each
    specs: Dict[str, Dict[str, Any]] = {
        endpoint: {
            "kind": endpoint.rstrip("s"),  # plural to singular bcas it's a column
            "id_field": id_field,
            "display_field": display_field,
            "data": [
                {id_field: row[id_field], display_field: row[display_field]}
                for row in call_endpoint(endpoint)
                if row
            ],
        }
        # These serve multiple purposes: names of endpoints, and names of columns
        for endpoint, (id_field, display_field) in dict(
            # endpoint = (id_field, display_field)
            filters=("name", "display_name"),
            custom_dimensions=("id", "display_name"),
            cohort_metrics=("name", "display_name"),
            conversion_metrics=("name", "display_name"),
            skan_events=("name", "display_name"),
            apps=("app_id", "app"),
            all_partners=("singular_partner_id", "singular_partner_display_name"),
        ).items()
    }
    # Right now the 'data' field has our desired granularity for `id` and `display`,
    # but we need the other 3 columns to apply for each row, we flatten it.
    data = {
        endpoint: [
            {
                "kind": attr["kind"],
                "id_field": attr["id_field"],
                "display_field": attr["display_field"],
                "id": row[attr["id_field"]],
                "display": row[attr["display_field"]],
            }
            for row in attr["data"]
            if row
        ]
        for endpoint, attr in specs.items()
    }
    # We don't care about the endpoint names anymore because they're in 'kind'
    # so flatten it with [i for s in [] for i in s]
    rows = [
        item for sublist in [data[endpoint] for endpoint in data] for item in sublist
    ]
    df = pd.DataFrame(rows)
    df.id = df.id.astype(str)
    df["column"] = df.id.copy()

    df.loc[
        df.id.astype(str).str.contains(r"[0-9]{2,}", regex=True), "column"
    ] = df.display.apply(format_variable)

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    import pickle
    with open("test_get_custom.pkl", "wb") as f:
        pickle.dump(df, f)

    return df


def get_custom_fields_unique_flagged(*args, df=None, **kwargs) -> pd.DataFrame:
    """
    The `get_custom_fields` function duplicate names and display names
    across different kinds of custom fields because they have different
    IDs.

    This function discards `id`, `id_field`, and `display_field` columns,
    then creates dummy/flag columns for each kind of custom field. This way,
    it can aggregate by actual unique fields and reveal overlap between kinds.
    """
    if df is None:
        df = get_custom_fields(*args, **kwargs)

    df = df[['kind', 'display', 'column']]

    for kind in df.kind.drop_duplicates().dropna():
        df[kind] = np.where(
            df.kind == kind, True, False
        )

    df.drop(columns=['kind'], inplace=True)
    df = df.groupby(['display','column'], as_index=False).agg('any')
    return df


def delay(func: Callable, seconds: float, *args, **kwargs) -> Any:
    import time
    time.sleep(seconds)
    return func(*args, **kwargs)


def pretty_time(t: float) -> str:
    """
    1616284202.0 -> "5/21 4:23:22 PM"
    """
    import datetime

    return datetime.datetime.fromtimestamp(t).strftime("%I:%M:%S %p, %m/%d")


def format_variable(s: str) -> str:
    """
    " ThisText   (x) is a__str " -> "this_text_x_is_a__str"
    """
    import re

    # Find camelCase and underscore delimit it before we mess with case
    s = re.sub(r"([a-z])([A-Z])", r"\1_\2", s)
    s = s.strip().lower()
    s = re.sub(r"-", " ", s)
    s = re.sub(r" [^A-Za-z] ", " ", s)  # " - " -> " "
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^A-Za-z0-9_ ]+", "", s)
    s = s.replace(" ", "_")
    return s


def format_constant(s: str) -> str:
    """
    "xX" -> "X_X"
    """
    s = format_variable(s)
    s = re.sub(r"([^A-Z_])([A-Z])", r"\1_\2", s)
    return s.upper()


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

    s = format_variable(s)
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


def read_raw_html(
    raw_html: Optional[str] = None, default: Optional[str] = None
) -> pd.DataFrame:
    if not raw_html and default:
        dfs = pd.read_html(default)
    elif len(raw_html) < 200:
        with open(raw_html, "r") as f:
            dfs = pd.read_html(f.read())
    else:
        dfs = pd.read_html(raw_html)
    assert len(dfs) >= 1, "No tables found in HTML"
    assert len(dfs) == 1, "Multiple tables found in HTML"
    return dfs[0]


# INTERNAL UTILITY FUNCTIONS
# ==============================================================================

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


if __name__ == "__main__":
    get_custom_fields()

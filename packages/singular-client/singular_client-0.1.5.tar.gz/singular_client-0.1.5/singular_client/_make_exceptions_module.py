"""
Threw this together to make the exceptions module dynamically by pasting in
the HTML from the Singular errors section at the bottom of Reporting API reference.
"""
from typing import Optional
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.min_rows", None)
from singular_client.utils import read_raw_html

def main():
    df = read_html()
    code = generate_python_module(df)
    with open("exceptions.py", "w") as f:
        f.write(code)

    return df, code


def generate_python_module(df):

    def match_err_map_doc(row):
        for err_map_doc in error_map_docs:
            if eval(err_map_doc.func)(row.text.lower()):
                return err_map_doc
        return None

    df["err_map_doc"] = df.apply(match_err_map_doc, axis=1)
    assert len(df[df.err_map_doc.isnull()]) == 0, f"No match found for all rows, {df}"
    codes = list(df.code.unique())
    s = HEADER

    for code in codes:
        s += gen_err_code_cls(code)

    for row in df.itertuples():
        s += gen_err_map(row.err_map_doc.cls, row.text, row.code)

    s += "CODES = [" + ", ".join([str(code) for code in codes]) + "]\n\n"
    s += "error_map = [\n"
    for err_map in df.err_map_doc:
        s += f"    ErrorMap(\n        {err_map.cls},\n        {err_map.func},\n        '''{err_map.example}''',\n    ),\n"

    s += "]\n\n\n"

    s += gen_throw_cust_err()

    return s


def gen_throw_cust_err():
    return """def throw_custom_error(code: int, message: str):
    if code not in CODES:
        raise SingularError(f"{code}: {message}")
    for err_map in error_map:
        if err_map.func(message.lower()):
            raise err_map.cls(message)
    raise eval(f"Singular{code}Error")(message)


"""

def gen_err_code_cls(code):
    return f"""class Singular{code}Error(SingularError):
    code = {code}


"""

def gen_err_map(cls_name, text, code) -> str:
    return f'''class {cls_name}(Singular{code}Error):
    msg = """ {text} """


'''


def read_html(raw_html: Optional[str] = None):
    df = read_raw_html(raw_html, default=_RAW_HTML_REPORTING)
    df.columns = df.iloc[0]
    df.drop(0, inplace=True)
    df.columns = [
        "code",
        "text",
        "extra_text",
    ]
    df.dropna(subset=["code", "text"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.code = df.code.astype(int)
    return df


HEADER = '''"""
EXCEPTIONS
==========

"""

from typing import Optional
from collections import namedtuple
ErrorMap = namedtuple("ErrorMap", ["cls", "func", "example"])

class SingularError(Exception):
    msg = ""
    code = None

    def __init__(self, message: Optional[str] = None, code: Optional[int] = None):
        m = message or self.msg
        c = code or self.code
        super().__init__(f"{c}: {m}")


'''
from collections import namedtuple
ErrorMap = namedtuple("ErrorMap", ["cls", "func", "example"])

error_map_docs = [
    # AUTHOR: GPT-4
    ErrorMap(
        'InvalidTimestamp',
        """lambda x: "timestamp" in x and "yyyy-mm-dd hh:mm:ss" in x""",
        "An invalid timestamp was given. The timestamp must be of the format: YYYY-MM-DD hh:mm:ss.",
    ),
    ErrorMap(
        "InvalidDate",
        """lambda x: "date" in x and "yyyy-mm-dd" in x""",
        "An invalid date was given. The date must be of the format: YYYY-MM-DD.",
    ),
    ErrorMap(
        "InvalidDateRange",
        """lambda x: "date range" in x and "later than" in x""",
        "An invalid date range was given. End date must be later than start date.",
    ),
    ErrorMap(
        "InvalidTimeBreakdown",
        """lambda x: "time breakdown" in x""",
        "An invalid time breakdown was given.",
    ),
    ErrorMap(
        "InvalidFilter",
        """lambda x: "invalid filter" in x""",
        "An invalid filter was given."
    ),
    ErrorMap(
        "MissingMetric",
        """lambda x: "one metric" in x and "must be used" in x""",
        "At least one metric must be used.",
    ),
    ErrorMap(
        "InvalidPublisherDimensions",
        """lambda x: "publisher dimensions" in x and "single day" in x""",
        "The requested data set includes publisher dimensions and extends beyond a single day. Please run single day queries with publisher dimensions.",
    ),
    ErrorMap(
        "InvalidResultFormat",
        """lambda x: "format" in x and "json" in x and "csv" in x""",
        "An invalid result format was given. Please select between JSON and CSV.",
    ),
    ErrorMap(
        "InvalidCountryCodeFormat",
        """lambda x: "country_code_format" in x""",
        'An invalid country_code_format was given. Please use "iso3" or "iso".',
    ),
    ErrorMap(
        "InvalidDimensions",
        """lambda x: "invalid dimensions" in x""",
        "The request contains invalid dimensions:",
    ),
    ErrorMap(
        "DuplicateFields",
        """lambda x: "duplicate fields" in x""",
        "The request contains duplicate fields: [list]",
    ),
    ErrorMap(
        "InvalidMetrics",
        """lambda x: "invalid metrics" in x""",
        "The request contains invalid metrics:",
    ),
    ErrorMap(
        "InvalidCohortPeriods",
        """lambda x: "invalid cohort periods" in x""",
        "The request contains invalid cohort periods:",
    ),
    ErrorMap(
        "MissingCohortPeriods",
        """lambda x: "cohort periods" in x and "cohort metrics" in x""",
        "We could not find cohort periods for the following cohort metrics: .",
    ),
    ErrorMap(
        "OldAPIVersion",
        """lambda x: "old api version" in x and "v2 api" in x""",
        "The request contains dimensions from an old API version: . Please use dimensions from the v2 API endpoint only.",
    ),
    ErrorMap(
        "MissingParameter",
        """lambda x: "missing the following parameter" in x""",
        "The request is missing the following parameter: .",
    ),
    ErrorMap(
        "InvalidAPIKey",
        """lambda x: "invalid api key" in x""",
        "An invalid API Key was given.",
    ),
    ErrorMap(
        "DeactivatedAPIKey",
        """lambda x: "api key" in x and "deactivated" in x""",
        "The provided API key has been previously deactivated. Please contact your administrator.",
    ),
    ErrorMap(
        "InsufficientAPIKeyPermissions",
        """lambda x: "api key" in x and "permissions" in x and "view the field" in x""",
        "The provided API key does not have permissions to view the field:",
    ),
    ErrorMap(
        "AccessDenied",
        """lambda x: "denied access" in x""",
        "The request is denied access. Please contact your administrator.",
    ),
    ErrorMap(
        "ReportIDNotFound",
        """lambda x: "report id" in x and "not found" in x""",
        "Report ID is not found. Please correct it or create a new report.",
    ),
    ErrorMap(
        "ReportIDMismatch",
        """lambda x: "report id" in x and "different key" in x""",
        "Report ID was created with a different key. Please use the same key when requesting status.",
    ),
    ErrorMap(
        "MethodNotAllowed",
        """lambda x: "method not allowed" in x""",
        "METHOD NOT ALLOWED"
    ),
    ErrorMap(
        "QueryQuotaExceeded",
        """lambda x: "query quota" in x and "exceeded" in x""",
        "Query quota is exceeded: only <> reports are currently allowed. The following report IDs are active: .",
    ),
    ErrorMap(
        "TooManyRequests",
        """lambda x: "too many requests" in x""",
        "Too many requests. Only <> requests per second is currently allowed.",
    ),
    ErrorMap(
        "InternalError",
        """lambda x: "failed" in x and "internal error" in x""",
        "The request has failed due to an internal error.",
    ),
]


_TEST_EXCEPTION_MAPS = """def test_exception_mappers():
    for mapper in exception_mappers:
        assert mapper.func(
            mapper.example.lower()
        ), f"{mapper.cls} failed to match its example"
"""









_RAW_HTML_REPORTING = """
<table class="table" style="font-size: small;">
<tbody>
<tr>
<td><strong>Code</strong></td>
<td><strong>Error Text</strong></td>
<td><strong>Additional Information</strong></td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid timestamp was given. The timestamp must be of the format: YYYY-MM-DD hh:mm:ss.</strong></td>
<td>Specify timestamps as in the following example: 2018-01-01 00:00:01</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid date was given. The date must be of the format: YYYY-MM-DD.</strong></td>
<td>Specify dates as in the following example: 2018-01-20</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid date range was given. End date must be later than start date.</strong></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid time breakdown was given.</strong></td>
<td>The time breakdown parameter is either missing in your query or isn't one of the supported options: "day", "week", "month", or "all".</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid filter was given.</strong></td>
<td>Use the Filters endpoint to get the list of filters you can use in your queries.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>At least one metric must be used.</strong></td>
<td>Include at least one metric in your query.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The requested data set includes publisher dimensions and extends beyond a single day. Please run single day queries with publisher dimensions.</strong></td>
<td>Reports broken down by publisher include large volumes of data. To run these reports, limit them to one day.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid result format was given. Please select between JSON and CSV.</strong></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>An invalid country_code_format was given. Please use "iso3" or "iso".</strong></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request contains invalid dimensions:</strong></td>
<td>One or more dimensions you requested in the query are either deprecated or invalid. If you used custom dimensions, double-check that they are available (using the custom dimensions endpoint) and make sure you used the dimension IDs (rather than their display names).</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request contains duplicate fields: [list]</strong></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request contains invalid metrics:</strong></td>
<td>One or more metrics you requested in the query are either deprecated or invalid. If you used cohort metrics or conversion events, double-check that they are available (using the cohort metrics and conversion events endpoints) and make sure you used the metric names (rather than their display names).</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request contains invalid cohort periods:</strong></td>
<td>Use the cohort metrics endpoints to check which cohort periods are available for your account.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>We could not find cohort periods for the following cohort metrics: .</strong></td>
<td>Add cohort periods for your cohort metrics.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request contains dimensions from an old API version: . Please use dimensions from the v2 API endpoint only.</strong></td>
<td>The request included dimensions from multiple API versions, which is not supported.</td>
</tr>
<tr>
<td><strong>400</strong></td>
<td><strong>The request is missing the following parameter: .</strong></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><strong>401</strong></td>
<td><strong>An invalid API Key was given.</strong></td>
<td>The API key is either missing or invalid. To get your API key, log into your Singular account and go to <strong>Developer Tools &gt; API Keys</strong>.</td>
</tr>
<tr>
<td><strong>401</strong></td>
<td><strong>The provided API key has been previously deactivated. Please contact your administrator.</strong></td>
<td>You are using an API key that belonged to a deactivated user. To get your API key, log into your Singular account and go to <strong>Developer Tools &gt; API Keys</strong>.</td>
</tr>
<tr>
<td><strong>403</strong></td>
<td><strong>The provided API key does not have permissions to view the field:<br></strong></td>
<td>The API key provided does not have permissions to view a dimension or metric you requested. Contact your organization's administrator to make sure you have the permissions you need.</td>
</tr>
<tr>
<td><strong>403</strong></td>
<td><strong>The request is denied access. Please contact your administrator.</strong></td>
<td>The request is denied. Contact your organization's administrator for further information.</td>
</tr>
<tr>
<td><strong>404</strong></td>
<td><strong>Report ID is not found. Please correct it or create a new report.</strong></td>
<td>Double-check that you used the Report ID returned from the Create Async Report endpoint. If the error persists, create a new report.</td>
</tr>
<tr>
<td><strong>404</strong></td>
<td><strong>Report ID was created with a different key. Please use the same key when requesting status.</strong></td>
<td>To query for a report status, you must use the same API key you used to generate the report.</td>
</tr>
<tr>
<td><strong>405</strong></td>
<td><strong>METHOD NOT ALLOWED</strong></td>
<td>You are probably using GET instead of POST or vice versa in your http request.</td>
</tr>
<tr>
<td><strong>429</strong></td>
<td><strong>Query quota is exceeded: only &lt;&gt; reports are currently allowed. The following report IDs are active: .</strong></td>
<td>You have exceeded the amount of async reports you are permitted to run at the same time. Wait for your previous requests to complete.</td>
</tr>
<tr>
<td><strong>429</strong></td>
<td><strong>Too many requests. Only &lt;&gt; requests per second is currently allowed.</strong></td>
<td>You have exceeded the rate limit. Wait for your previous requests to complete.</td>
</tr>
<tr>
<td><strong>500</strong></td>
<td><strong>The request has failed due to an internal error.</strong></td>
<td>Typically, this just means you should retry your API call. See <a href="https://support.singular.net/hc/en-us/articles/360028754072#500_error" target="_self">What should I do if I get a 500 error?</a></td>
</tr>
</tbody>
</table>
"""


if __name__ == "__main__":
    main()

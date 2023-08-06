"""
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


class Singular400Error(SingularError):
    code = 400


class Singular401Error(SingularError):
    code = 401


class Singular403Error(SingularError):
    code = 403


class Singular404Error(SingularError):
    code = 404


class Singular405Error(SingularError):
    code = 405


class Singular429Error(SingularError):
    code = 429


class Singular500Error(SingularError):
    code = 500


class InvalidTimestamp(Singular400Error):
    msg = """ An invalid timestamp was given. The timestamp must be of the format: YYYY-MM-DD hh:mm:ss. """


class InvalidDate(Singular400Error):
    msg = """ An invalid date was given. The date must be of the format: YYYY-MM-DD. """


class InvalidDateRange(Singular400Error):
    msg = """ An invalid date range was given. End date must be later than start date. """


class InvalidTimeBreakdown(Singular400Error):
    msg = """ An invalid time breakdown was given. """


class InvalidFilter(Singular400Error):
    msg = """ An invalid filter was given. """


class MissingMetric(Singular400Error):
    msg = """ At least one metric must be used. """


class InvalidPublisherDimensions(Singular400Error):
    msg = """ The requested data set includes publisher dimensions and extends beyond a single day. Please run single day queries with publisher dimensions. """


class InvalidResultFormat(Singular400Error):
    msg = """ An invalid result format was given. Please select between JSON and CSV. """


class InvalidCountryCodeFormat(Singular400Error):
    msg = """ An invalid country_code_format was given. Please use "iso3" or "iso". """


class InvalidDimensions(Singular400Error):
    msg = """ The request contains invalid dimensions: """


class DuplicateFields(Singular400Error):
    msg = """ The request contains duplicate fields: [list] """


class InvalidMetrics(Singular400Error):
    msg = """ The request contains invalid metrics: """


class InvalidCohortPeriods(Singular400Error):
    msg = """ The request contains invalid cohort periods: """


class MissingCohortPeriods(Singular400Error):
    msg = """ We could not find cohort periods for the following cohort metrics: . """


class OldAPIVersion(Singular400Error):
    msg = """ The request contains dimensions from an old API version: . Please use dimensions from the v2 API endpoint only. """


class MissingParameter(Singular400Error):
    msg = """ The request is missing the following parameter: . """


class InvalidAPIKey(Singular401Error):
    msg = """ An invalid API Key was given. """


class DeactivatedAPIKey(Singular401Error):
    msg = """ The provided API key has been previously deactivated. Please contact your administrator. """


class InsufficientAPIKeyPermissions(Singular403Error):
    msg = """ The provided API key does not have permissions to view the field: """


class AccessDenied(Singular403Error):
    msg = """ The request is denied access. Please contact your administrator. """


class ReportIDNotFound(Singular404Error):
    msg = """ Report ID is not found. Please correct it or create a new report. """


class ReportIDMismatch(Singular404Error):
    msg = """ Report ID was created with a different key. Please use the same key when requesting status. """


class MethodNotAllowed(Singular405Error):
    msg = """ METHOD NOT ALLOWED """


class QueryQuotaExceeded(Singular429Error):
    msg = """ Query quota is exceeded: only <> reports are currently allowed. The following report IDs are active: . """


class TooManyRequests(Singular429Error):
    msg = """ Too many requests. Only <> requests per second is currently allowed. """


class InternalError(Singular500Error):
    msg = """ The request has failed due to an internal error. """


CODES = [400, 401, 403, 404, 405, 429, 500]

error_map = [
    ErrorMap(
        InvalidTimestamp,
        lambda x: "timestamp" in x and "yyyy-mm-dd hh:mm:ss" in x,
        '''An invalid timestamp was given. The timestamp must be of the format: YYYY-MM-DD hh:mm:ss.''',
    ),
    ErrorMap(
        InvalidDate,
        lambda x: "date" in x and "yyyy-mm-dd" in x,
        '''An invalid date was given. The date must be of the format: YYYY-MM-DD.''',
    ),
    ErrorMap(
        InvalidDateRange,
        lambda x: "date range" in x and "later than" in x,
        '''An invalid date range was given. End date must be later than start date.''',
    ),
    ErrorMap(
        InvalidTimeBreakdown,
        lambda x: "time breakdown" in x,
        '''An invalid time breakdown was given.''',
    ),
    ErrorMap(
        InvalidFilter,
        lambda x: "invalid filter" in x,
        '''An invalid filter was given.''',
    ),
    ErrorMap(
        MissingMetric,
        lambda x: "one metric" in x and "must be used" in x,
        '''At least one metric must be used.''',
    ),
    ErrorMap(
        InvalidPublisherDimensions,
        lambda x: "publisher dimensions" in x and "single day" in x,
        '''The requested data set includes publisher dimensions and extends beyond a single day. Please run single day queries with publisher dimensions.''',
    ),
    ErrorMap(
        InvalidResultFormat,
        lambda x: "format" in x and "json" in x and "csv" in x,
        '''An invalid result format was given. Please select between JSON and CSV.''',
    ),
    ErrorMap(
        InvalidCountryCodeFormat,
        lambda x: "country_code_format" in x,
        '''An invalid country_code_format was given. Please use "iso3" or "iso".''',
    ),
    ErrorMap(
        InvalidDimensions,
        lambda x: "invalid dimensions" in x,
        '''The request contains invalid dimensions:''',
    ),
    ErrorMap(
        DuplicateFields,
        lambda x: "duplicate fields" in x,
        '''The request contains duplicate fields: [list]''',
    ),
    ErrorMap(
        InvalidMetrics,
        lambda x: "invalid metrics" in x,
        '''The request contains invalid metrics:''',
    ),
    ErrorMap(
        InvalidCohortPeriods,
        lambda x: "invalid cohort periods" in x,
        '''The request contains invalid cohort periods:''',
    ),
    ErrorMap(
        MissingCohortPeriods,
        lambda x: "cohort periods" in x and "cohort metrics" in x,
        '''We could not find cohort periods for the following cohort metrics: .''',
    ),
    ErrorMap(
        OldAPIVersion,
        lambda x: "old api version" in x and "v2 api" in x,
        '''The request contains dimensions from an old API version: . Please use dimensions from the v2 API endpoint only.''',
    ),
    ErrorMap(
        MissingParameter,
        lambda x: "missing the following parameter" in x,
        '''The request is missing the following parameter: .''',
    ),
    ErrorMap(
        InvalidAPIKey,
        lambda x: "invalid api key" in x,
        '''An invalid API Key was given.''',
    ),
    ErrorMap(
        DeactivatedAPIKey,
        lambda x: "api key" in x and "deactivated" in x,
        '''The provided API key has been previously deactivated. Please contact your administrator.''',
    ),
    ErrorMap(
        InsufficientAPIKeyPermissions,
        lambda x: "api key" in x and "permissions" in x and "view the field" in x,
        '''The provided API key does not have permissions to view the field:''',
    ),
    ErrorMap(
        AccessDenied,
        lambda x: "denied access" in x,
        '''The request is denied access. Please contact your administrator.''',
    ),
    ErrorMap(
        ReportIDNotFound,
        lambda x: "report id" in x and "not found" in x,
        '''Report ID is not found. Please correct it or create a new report.''',
    ),
    ErrorMap(
        ReportIDMismatch,
        lambda x: "report id" in x and "different key" in x,
        '''Report ID was created with a different key. Please use the same key when requesting status.''',
    ),
    ErrorMap(
        MethodNotAllowed,
        lambda x: "method not allowed" in x,
        '''METHOD NOT ALLOWED''',
    ),
    ErrorMap(
        QueryQuotaExceeded,
        lambda x: "query quota" in x and "exceeded" in x,
        '''Query quota is exceeded: only <> reports are currently allowed. The following report IDs are active: .''',
    ),
    ErrorMap(
        TooManyRequests,
        lambda x: "too many requests" in x,
        '''Too many requests. Only <> requests per second is currently allowed.''',
    ),
    ErrorMap(
        InternalError,
        lambda x: "failed" in x and "internal error" in x,
        '''The request has failed due to an internal error.''',
    ),
]


def throw_custom_error(code: int, message: str):
    if code not in CODES:
        raise SingularError(f"{code}: {message}")
    for err_map in error_map:
        if err_map.func(message.lower()):
            raise err_map.cls(message)
    raise eval(f"Singular{code}Error")(message)



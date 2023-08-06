from singular_client._bases import _Endpoint, ResponseDocList
from singular_client.documents import *
from singular_client.arguments import *
from singular_client.endpoints.reporting import CreateReportResponse
from typing import *
from singular_client.utils import _convert_list_arg


class SkanEventsEndpoint(_Endpoint[ResponseDocList[NameDoc]]):
    endpoint = "v2.0/skan_events"
    data_path = ["value", "skan_events"]
    res_type = ResponseDocList[NameDoc]


class SkanRawReportEndpoint(_Endpoint[CreateReportResponse]):
    endpoint = "v2.0/create_async_skadnetwork_raw_report"
    data_path = ["value", "report_id"]
    available_dimensions = SKAN_RAW_DIMENSIONS
    available_metrics = SKAN_RAW_METRICS
    res_type = CreateReportResponse
    returns_collection = False
    method = "POST"

    def request(
        self,
        start_date: str,
        time_breakdown: TimeBreakdown = "all",
        end_date: Optional[str] = None,
        skadnetwork_date_type: SkadDateType = "skan_postback_date",
        dimensions: Optional[Union[List[SkanRawDimension], str]] = None,
        metrics: Optional[Union[List[SkanRawMetric], str]] = None,
        app: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        filters: Optional[List[dict]] = None,
        format: FileFormat = "csv",
        country_code_format: CountryCodeFormat = "iso3",
    ):
        report_id = super().request(
            data=dict(
                start_date=start_date,
                end_date=end_date or start_date,
                time_breakdown=time_breakdown,
                skadnetwork_date_type=skadnetwork_date_type,
                dimensions=_convert_list_arg(dimensions, self.available_dimensions),
                metrics=_convert_list_arg(metrics, self.available_metrics),
                app=_convert_list_arg(app),
                source=_convert_list_arg(source),
                filters=filters,
                format=format,
                country_code_format=country_code_format,
            ),
        )
        report_id.api = self.api
        return report_id


class SkanReportEndpoint(_Endpoint[CreateReportResponse]):
    endpoint = "v2.0/create_async_skadnetwork_report"
    data_path = ["value", "report_id"]
    res_type = CreateReportResponse
    available_dimensions = SKAN_DIMENSIONS
    available_metrics = SKAN_METRICS
    returns_collection = False
    method = "POST"

    def request(
        self,
        start_date: str,
        time_breakdown: TimeBreakdown = "all",
        end_date: Optional[str] = None,
        skadnetwork_date_type: SkadDateType = "skan_postback_date",
        dimensions: Optional[Union[List[SkanDimension], str]] = None,
        metrics: Optional[Union[List[SkanMetric], str]] = None,
        skan_events: Optional[List[str]] = None,
        format: FileFormat = "csv",
    ):
        report_id = super().request(
            data=dict(
                start_date=start_date,
                end_date=end_date or start_date,
                time_breakdown=time_breakdown,
                skadnetwork_date_type=skadnetwork_date_type,
                dimensions=_convert_list_arg(dimensions, self.available_dimensions),
                metrics=_convert_list_arg(metrics, self.available_metrics),
                skan_events=_convert_list_arg(skan_events),
                format=format,
            ),
        )
        report_id.api = self.api
        return report_id

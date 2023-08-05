from singular.endpoints._bases import _Endpoint, ResponseDocList
from singular.documents import *
from singular.arguments import *
from typing import *
from singular._utils import *

class AdMonetizationEndpoint(_Endpoint[ResponseDocList[AdMonetizationDoc]]):
    endpoint = "v2.0/admonetization/reporting"
    data_path = ["value", "results"]
    res_type = ResponseDocList[AdMonetizationDoc]

    def request(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        time_breakdown: TimeBreakdown = "all",
        dimensions: Optional[Union[List[AdMonDimension], str]] = None,
        metrics: Optional[Union[List[AdMonMetric], str]] = None,
        app: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        filters: Optional[List[dict]] = None,
        format: FileFormat = "json",
        country_code_format: CountryCodeFormat = "iso3",
    ):
        return super().request(
            start_date=start_date,
            end_date=end_date or start_date,
            time_breakdown=time_breakdown,
            dimensions=convert_list_arg(dimensions, AD_MON_DIMENSIONS),
            metrics=convert_list_arg(metrics, AD_MON_METRICS),
            app=convert_list_arg(app),
            source=convert_list_arg(source),
            filters=filters,
            format=format,
            country_code_format=country_code_format,
        )



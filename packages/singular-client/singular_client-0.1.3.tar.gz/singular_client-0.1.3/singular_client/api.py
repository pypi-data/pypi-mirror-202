from __future__ import annotations
import requests
from typing import (
    Optional,
    Literal,
)
import os

from singular_client.documents import *
from singular_client.arguments import *


class SingularAPI:
    """
    A simple class to store endpoint instances, and handle authentication and base url
    when requesting data from the Singular API.

    Passes a reference to itself to each endpoint instance, so that they can access
    the request method.
    """

    base_url = "https://api.singular.net/api/"
    logs = True

    key: str

    def __init__(self, key: Optional[str]=None):
        if not key:
            key = os.environ.get("SINGULAR_API_KEY")
            assert key, "No API key provided"
        self.key = key

        from singular_client import endpoints

        # Reporting
        self.combined_report = endpoints.CombinedReportEndpoint(self)
        self.network_report = endpoints.NetworkReportEndpoint(self)
        self.tracker_report = endpoints.TrackerReportEndpoint(self)
        self.data_availability = endpoints.DataAvailabilityEndpoint(self)
        self.report_status = endpoints.ReportStatusEndpoint(self)
        self.filters = endpoints.FiltersEndpoint(self)
        self.custom_dimensions = endpoints.CustomDimensionsEndpoint(self)
        self.cohort_metrics = endpoints.CohortMetricsEndpoint(self)
        self.conversion_metrics = endpoints.ConversionMetricsEndpoint(self)

        # SKAdNetwork
        self.skan_raw_report = endpoints.SkanRawReportEndpoint(self)
        self.skan_report = endpoints.SkanReportEndpoint(self)
        self.skan_events = endpoints.SkanEventsEndpoint(self)

        # Links
        self.create_link = endpoints.CreateLinkEndpoint(self)
        self.view_links = endpoints.ViewLinksEndpoint(self)
        self.apps = endpoints.AppsEndpoint(self)
        self.configured_partners = endpoints.ConfiguredPartnersEndpoint(self)
        self.domains = endpoints.DomainsEndpoint(self)
        self.all_partners = endpoints.AllPartnersEndpoint(self)

        # Links (Legacy)
        self.discover_apps_legacy = endpoints.AppsLegacyEndpoint(self)
        self.available_partners_legacy = endpoints.AvailablePartnersLegacyEndpoint(self)
        self.link_legacy = endpoints.CreateLinkLegacyEndpoint(self)
        self.view_links_legacy = endpoints.ViewLinksLegacyEndpoint(self)
        self.custom_link_legacy = endpoints.CreateCustomLinkLegacyEndpoint(self)
        self.view_custom_links_legacy = endpoints.ViewCustomLinksLegacyEndpoint(self)

        # Ad Monetization
        self.ad_monetization = endpoints.AdMonetizationEndpoint(self)

        # Governance (graphql)
        self.graphql = endpoints.GraphQL(self)

    def request(
        self,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
        params=None,
        headers=None,
        data=None,
        key_in_headers: Optional[bool] = None,
    ) -> dict:
        url = self.base_url + endpoint

        # Default to None instead of dict because mutable defaults persist
        if not params:
            params = dict()
        if not headers:
            headers = dict()
        if not data:
            data = dict()

        # We can usually determine where to place auth key by checking if it's
        # a v1 endpoint. `key_in_headers` can be used to override this.
        if key_in_headers is None:
            key_in_headers = "v1" in url

        if key_in_headers:
            headers["Authorization"] = self.key
        else:
            params["api_key"] = self.key

        res = requests.request(
            method, url=url, params=params, headers=headers, data=data
        )

        assert (code := res.status_code) == 200, (code, res.text)

        # return UtilDict(res.json()).deep_uniform()
        return res.json()

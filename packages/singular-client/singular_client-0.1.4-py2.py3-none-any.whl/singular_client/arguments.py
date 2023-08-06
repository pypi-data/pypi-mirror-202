"""
VALID PARAMETER TYPES FOR ENDPOINTS
===================================

T

Use cases
---------

Static type checking
    Any endpoint parameter for which there is a fixed set of valid values is
    typed as a Literal. Your IDE will statically check that you are passing
    valid options and bark at you otherwise. Parameters that require a list of
    valid values (dimensions and metrics) allow you to override this behavior
    by joining options to a comma-sep string before passing.

Filling default values
    The arguments stored in each Literal are also stored as regular lists (see
    bottom of file). These are used to fill in default values for parameters
    that are left empty. For instance, any endpoint which requires a list of
    dimensions or metrics will defualt to returning all available attributes
    if param is left null.

Easy user-access to available options for an endpoint
    Endpoints which require a list of valid dimensions or metrics will have
    a `available_dimensions` class attribute, etc.


Notes
-----
When a parameter requires a list of valid Literal options, (rather than
just a single one), your type checker will be unhappy if you pass this list
as a variable, rather than a hardcoded list. These parameters also accept
a string, so you can override this behavior by joining the list first.
"""
from typing import Literal, get_args

TimeBreakdown = Literal["day", "week", "month", "all"]
FileFormat = Literal["json", "csv"]
CountryCodeFormat = Literal["iso3", "iso"]
LinkType = Literal["custom", "partner", "mobile_web_to_app"]
SkadDateType = Literal["skan_postback_date", "estimated_install_date"]


CombinedDimension = Literal[
    # Basic dimensions (should be available for all networks and trackers)
    "app",
    "source",
    "unified_campaign_id",
    "unified_campaign_name",
    # Optional additional dimensions (support varies by network/tracker)
    "os",
    "platform",
    "country_field",
    "adn_sub_adnetwork_name",
    "adn_account_id",
    "adn_account_name",
    "sub_campaign_name",
    # Keyword and/or publisher breakdown (support varies by network/tracker, cannot be pulled in the same query as creative breakdown)
    "keyword_id",
    "keyword",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    # Creative breakdown (support varies by network, only available for users of Singular's attribution service)
    "creative_type",
    "adn_creative_id",
    "adn_creative_name",
    "creative_url",
    "creative_image",
    "creative_text",
    "creative_width",
    "creative_height",
    "creative_is_video",
]

CombinedMetric = Literal[
    # Basic metrics
    "adn_cos",
    "adn_original_cost",
    "adn_original_currency",
    "custom_impressions",
    "custom_clicks",
    "custom_installs",
    "tracker_conversions",
    "tracker_reengagements",
    "daily_active_users",
    # Metrics for video creatives and video-based campaigns
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
    "completed_video_views",
    "completed_video_view_rate",
]

NetworkDimension = Literal[
    # Basic dimensions (should be available for all networks):
    "app",
    "source",
    "adn_campaign_id",
    "adn_campaign_name",
    "adn_campaign_url",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_username",
    "data_connector_timestamp_utc",
    # Optional additional dimensions (support varies by network):
    "os",
    "platform",
    "country_field",
    "region_field",
    "city_field",
    "dma_id_field",
    "dma_name_field",
    "adn_sub_adnetwork_name",
    "adn_account_id",
    "adn_account_name",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    # Keyword and/or publisher breakdown (support varies by network, cannot be pulled in the same query as creative breakdown):
    "keyword_id",
    "keyword",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    # Creative breakdown (support varies by network, usually cannot be pulled in the same query as keyword/publisher):
    "creative_type",
    "adn_creative_id",
    "adn_creative_name",
    "creative_url",
    "creative_image",
    "creative_text",
    "creative_width",
    "creative_height",
    "creative_is_video",
    "asset_id",
    "asset_name",
    # Campaign properties:
    "bid_type",
    "bid_strategy",
    "bid_amount",
    "campaign_objective",
    "standardized_bid_type",
    "standardized_bid_strategy",
    "original_bid_amount",
    "campaign_status",
    "min_roas",
    "original_metadata_currency",
]

NetworkMetric = Literal[
    "adn_cost",
    "adn_original_cost",
    "adn_original_currency",
    "adn_impressions",
    "adn_clicks",
    "adn_installs",
]

TrackerDimension = Literal[
    # Basic dimensions (should be available for all networks):
    "app",
    "source",
    "tracker_campaign_id",
    # Optional additional dimensions (support varies by tracker):
    "tracker_campaign_name",
    "os",
    "platform",
    "country_field",
]

TrackerMetric = Literal[
    # Basic metrics:
    "tracker_impressions",
    "tracker_clicks",
    "tracker_installs",
    "tracker_conversions",
    "tracker_reengagements",
    "daily_active_users",
    # Cohort metrics:
    "revenue",
    "original_revenue",
]


StandardCohortMetric = Literal[
    "revenue",
    "original_revenue",
]


SkanDimension = Literal[
    "source",
    "app",
    "country_field",
    "skan_redownloads",
    "skan_validated",
    "unified_campaign_id",
    "unified_campaign_name",
]

SkanMetric = Literal[
    "adn_cost",
    "ctr",
    "skan_conversion_values_count",
    "skan_conversion_values_ratio",
    "skan_revenue",
    "skan_roi",
    "skan_installs",
    "skan_ecpi",
    "skan_ocvr",
    "skan_report_network_clicks",
    "skan_report_network_impressions",
    "tracker_installs",
]

SkanRawDimension = Literal[
    "skan_app_id",
    "skan_network_id",
    "skan_campaign_id",
    "skan_publisher_id",
    "app",
    "source",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "country_field",
    "skan_conversion_value",
    "skan_redownloads",
    "skan_validated",
    "skan_version",
]

SkanRawMetric = Literal[
    "skan_installs",
    "skan_p2_postbacks",
    "skan_p3_postbacks",
    "skan_conversion_values_count",
    "skan_conversion_values_ratio",
    "skan_p2_ratio",
    "skan_p3_ratio",
    # "modeled_conversion_value_count",
    # "modeled_conversion_value_count_confidence_interval",
]

AdMonDimension = Literal[
    "source",
    "app",
    "os",
    "platform",
    "site_public_id" "ad_country",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "instance_id",
    "instance_name",
    "custom_dimension_id",
]

AdMonMetric = Literal[
    "ad_requests",
    "filled_ad_requests",
    "ad_fill_rate",
    "ad_impressions",
    "video_views",
    "completed_video_views",
    "completed_video_view_rate",
    "ad_clicks",
    "ad_ecpm",
    "ad_ecpv",
    "ad_ecpcv",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
]

ValidDimension = Literal[
    "adn_account_id",
    "adn_account_name",
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
    "asset_id",
    "asset_name",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "adn_campaign_url",
    "city_field",
    "adn_click_type",
    "conversion_type",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "ad_country",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "device_model",
    "dma_id_field",
    "dma_name_field",
    "fb_adset_id",
    "fb_campaign_id",
    "min_roas",
    "final_url",
    "installer_source",
    "is_uac",
    "keyword",
    "keyword_id",
    "keyword_match_type",
    "adn_campaign_id",
    "adn_campaign_name",
    "adn_creative_id",
    "adn_creative_name",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "creative_type",
    "install_app_store",
    "original_bid_amount",
    "original_ metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "skan_redownloads",
    "retention",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracking_url",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_creative_id",
    "tracker_creative_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_ name",
    "adn_utc_offset",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
    "skan_validated",
    "admon_data_source",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
    "singular_creative_id",
]

ValidDimension = Literal[
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "frequency",
    "bid_requests",
    "bid_responses",
    "custom_clicks",
    "skan_report_network_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "completed_video_views",
    "ad_completed_video_views",
    "skan_conversion_values_count",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "filled_ad_requests",
    "custom_impressions",
    "skan_report_network_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "new_visitors",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "re_engaged_visitors",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "total_revenue",
    "total_web_conversions",
    "tracker_clicks",
    "tracker_installs",
    "video_views",
    "ad_video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

ValidColumn = Literal[
    "adn_account_id",
    "adn_account_name",
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
    "asset_id",
    "asset_name",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "adn_campaign_url",
    "city_field",
    "adn_click_type",
    "conversion_type",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "ad_country",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "device_model",
    "dma_id_field",
    "dma_name_field",
    "fb_adset_id",
    "fb_campaign_id",
    "min_roas",
    "final_url",
    "installer_source",
    "is_uac",
    "keyword",
    "keyword_id",
    "keyword_match_type",
    "adn_campaign_id",
    "adn_campaign_name",
    "adn_creative_id",
    "adn_creative_name",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "creative_type",
    "install_app_store",
    "original_bid_amount",
    "original_ metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "skan_redownloads",
    "retention",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracking_url",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_creative_id",
    "tracker_creative_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_ name",
    "adn_utc_offset",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
    "skan_validated",
    "admon_data_source",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
    "singular_creative_id",
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "frequency",
    "bid_requests",
    "bid_responses",
    "custom_clicks",
    "skan_report_network_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "completed_video_views",
    "ad_completed_video_views",
    "skan_conversion_values_count",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "filled_ad_requests",
    "custom_impressions",
    "skan_report_network_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "new_visitors",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "re_engaged_visitors",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "total_revenue",
    "total_web_conversions",
    "tracker_clicks",
    "tracker_installs",
    "video_views",
    "ad_video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

TIME_BREAKDOWNS = list(get_args(TimeBreakdown))
FILE_FORMATS = list(get_args(FileFormat))
COUNTY_CODE_FORMATS = list(get_args(CountryCodeFormat))
LINK_TYPE = list(get_args(LinkType))
SKAD_DATE_TYPES = list(get_args(SkadDateType))
COMBINED_DIMENSIONS = list(get_args(CombinedDimension))
COMBINED_METRICS = list(get_args(CombinedMetric))
NETWORK_DIMENSIONS = list(get_args(NetworkDimension))
NETWORK_METRICS = list(get_args(NetworkMetric))
TRACKER_DIMENSIONS = list(get_args(TrackerDimension))
TRACKER_METRICS = list(get_args(TrackerMetric))
STANDARD_COHORT_METRICS = list(get_args(StandardCohortMetric))
SKAN_DIMENSIONS = list(get_args(SkanDimension))
SKAN_METRICS = list(get_args(SkanMetric))
SKAN_RAW_DIMENSIONS = list(get_args(SkanRawDimension))
SKAN_RAW_METRICS = list(get_args(SkanRawMetric))
AD_MON_DIMENSIONS = list(get_args(AdMonDimension))
AD_MON_METRICS = list(get_args(AdMonMetric))

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
    "skan_conversion_values_count",
    "skan_conversion_values_ratio",
    "skan_installs",
    "modeled_skan_conversion_values_count",
    "skan_p2_postbacks",
    "skan_p3_postbacks",
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

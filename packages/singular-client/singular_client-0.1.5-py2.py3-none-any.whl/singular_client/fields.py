"""
VALID PARAMETER TYPES FOR ENDPOINTS
===================================

    Instant, real-time, as-you-type checking of dimension/metric names in your IDE.


Defines Literal types, constant lists, and validator function for all combinations
of dimension and metric categories in Singular.

Literals allow your IDE to validate that the string you're typing is a valid
option for the type-hinted parameter you're passing args to.

Fields are broken down into 3 levels.

Every combination of these 3 levels has a corresponding Literal type, constant list,
validator function, and more.

Level 1
    Field
    Dimension
    Metric

Level 2  (Available in ...)
    InGeneral
    InCreative
    InSkan
    InSkanRaw
    InAdMon
    
Level 3  (Data came from ...)
    FromNetwork
    FromTracker

For each combination, define (using DimensionFromNetwork as an example):
    FromNetworkDimension
        A Literal string type with all valid dimensions that come from ad networks.
        When something is type-hinted with this, your IDE will, in real time as
        you're typing, validate that the string you've written is a valid option and
        instantly bark at you otherwise.
        USE CASE:
            Any endpoint parameter for which there is a fixed set of valid dimensions
            or metrics can be typed with the appropriate Literal type.

    FromNetworkDimensionArgs
        A Union type that accepts EITHER a list of these valid dimensions OR
        a string.
        USE CASE:
            For endpoints parameters that require a list of dimensions or metrics,
            this makes it easier for the user to override the type checking by
            simply string joining the list first.

    FROM_NETWORK_DIMENSION
        A constant list of all valid options for that combination.
        USE CASE:
            This can be used for internal validation of arguments (not recommended),
            or easy access by the user.

    is_from_network_dimension()
        A function that returns True if a given string is a valid network dimension.
        USE CASE:
            Can be used for internal validation of arguments (not recommended),
            or make it easier for the user to validate their own arguments.

"""

from typing import Literal, Iterable, Union, get_args


Field = Literal[
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
    "original_metadata_currency",
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
    "tracker_sub_campaign_name",
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

FieldArgs = Union[Iterable[Field], str]

FIELD = list(get_args(Field))

def is_field(name: Union[str, Field]) -> bool:
    """
    Check if `name` is a valid non-custom `Field` from Singular.
    """
    return name in FIELD


Dimension = Literal[
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
    "original_metadata_currency",
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
    "tracker_sub_campaign_name",
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

DimensionArgs = Union[Iterable[Dimension], str]

DIMENSION = list(get_args(Dimension))

def is_dimension(name: Union[str, Dimension]) -> bool:
    """
    Check if `name` is a valid non-custom `Dimension` from Singular.
    """
    return name in DIMENSION


DimensionInGeneral = Literal[
    "adn_account_id",
    "adn_account_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
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
    "country_field",
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
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracking_url",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
    "adn_utc_offset",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
]

DimensionInGeneralArgs = Union[Iterable[DimensionInGeneral], str]

DIMENSION_IN_GENERAL = list(get_args(DimensionInGeneral))

def is_dimension_in_general(name: Union[str, DimensionInGeneral]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInGeneral` from Singular.
    """
    return name in DIMENSION_IN_GENERAL


DimensionInGeneralFromNetwork = Literal[
    "adn_account_id",
    "adn_account_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
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
    "country_field",
    "device_model",
    "dma_id_field",
    "dma_name_field",
    "fb_adset_id",
    "fb_campaign_id",
    "min_roas",
    "final_url",
    "is_uac",
    "keyword",
    "keyword_id",
    "keyword_match_type",
    "adn_campaign_id",
    "adn_campaign_name",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracking_url",
    "adn_utc_offset",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
]

DimensionInGeneralFromNetworkArgs = Union[Iterable[DimensionInGeneralFromNetwork], str]

DIMENSION_IN_GENERAL_FROM_NETWORK = list(get_args(DimensionInGeneralFromNetwork))

def is_dimension_in_general_from_network(name: Union[str, DimensionInGeneralFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInGeneralFromNetwork` from Singular.
    """
    return name in DIMENSION_IN_GENERAL_FROM_NETWORK


DimensionInGeneralFromTracker = Literal[
    "app",
    "site_public_id",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "city_field",
    "conversion_type",
    "country_field",
    "min_roas",
    "installer_source",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "os",
    "platform",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
]

DimensionInGeneralFromTrackerArgs = Union[Iterable[DimensionInGeneralFromTracker], str]

DIMENSION_IN_GENERAL_FROM_TRACKER = list(get_args(DimensionInGeneralFromTracker))

def is_dimension_in_general_from_tracker(name: Union[str, DimensionInGeneralFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInGeneralFromTracker` from Singular.
    """
    return name in DIMENSION_IN_GENERAL_FROM_TRACKER


DimensionInCreative = Literal[
    "adn_account_id",
    "adn_account_name",
    "app",
    "asset_id",
    "asset_name",
    "unified_campaign_id",
    "unified_campaign_name",
    "adn_campaign_url",
    "adn_click_type",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "adn_creative_id",
    "adn_creative_name",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_creative_id",
    "tracker_creative_name",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
]

DimensionInCreativeArgs = Union[Iterable[DimensionInCreative], str]

DIMENSION_IN_CREATIVE = list(get_args(DimensionInCreative))

def is_dimension_in_creative(name: Union[str, DimensionInCreative]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInCreative` from Singular.
    """
    return name in DIMENSION_IN_CREATIVE


DimensionInCreativeFromNetwork = Literal[
    "adn_account_id",
    "adn_account_name",
    "app",
    "asset_id",
    "asset_name",
    "unified_campaign_id",
    "unified_campaign_name",
    "adn_campaign_url",
    "adn_click_type",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "adn_creative_id",
    "adn_creative_name",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
]

DimensionInCreativeFromNetworkArgs = Union[Iterable[DimensionInCreativeFromNetwork], str]

DIMENSION_IN_CREATIVE_FROM_NETWORK = list(get_args(DimensionInCreativeFromNetwork))

def is_dimension_in_creative_from_network(name: Union[str, DimensionInCreativeFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInCreativeFromNetwork` from Singular.
    """
    return name in DIMENSION_IN_CREATIVE_FROM_NETWORK


DimensionInCreativeFromTracker = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_creative_id",
    "tracker_creative_name",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
]

DimensionInCreativeFromTrackerArgs = Union[Iterable[DimensionInCreativeFromTracker], str]

DIMENSION_IN_CREATIVE_FROM_TRACKER = list(get_args(DimensionInCreativeFromTracker))

def is_dimension_in_creative_from_tracker(name: Union[str, DimensionInCreativeFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInCreativeFromTracker` from Singular.
    """
    return name in DIMENSION_IN_CREATIVE_FROM_TRACKER


DimensionInSkan = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanArgs = Union[Iterable[DimensionInSkan], str]

DIMENSION_IN_SKAN = list(get_args(DimensionInSkan))

def is_dimension_in_skan(name: Union[str, DimensionInSkan]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkan` from Singular.
    """
    return name in DIMENSION_IN_SKAN


DimensionInSkanFromNetwork = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanFromNetworkArgs = Union[Iterable[DimensionInSkanFromNetwork], str]

DIMENSION_IN_SKAN_FROM_NETWORK = list(get_args(DimensionInSkanFromNetwork))

def is_dimension_in_skan_from_network(name: Union[str, DimensionInSkanFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkanFromNetwork` from Singular.
    """
    return name in DIMENSION_IN_SKAN_FROM_NETWORK


DimensionInSkanFromTracker = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanFromTrackerArgs = Union[Iterable[DimensionInSkanFromTracker], str]

DIMENSION_IN_SKAN_FROM_TRACKER = list(get_args(DimensionInSkanFromTracker))

def is_dimension_in_skan_from_tracker(name: Union[str, DimensionInSkanFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkanFromTracker` from Singular.
    """
    return name in DIMENSION_IN_SKAN_FROM_TRACKER


DimensionInSkanRaw = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanRawArgs = Union[Iterable[DimensionInSkanRaw], str]

DIMENSION_IN_SKAN_RAW = list(get_args(DimensionInSkanRaw))

def is_dimension_in_skan_raw(name: Union[str, DimensionInSkanRaw]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkanRaw` from Singular.
    """
    return name in DIMENSION_IN_SKAN_RAW


DimensionInSkanRawFromNetwork = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanRawFromNetworkArgs = Union[Iterable[DimensionInSkanRawFromNetwork], str]

DIMENSION_IN_SKAN_RAW_FROM_NETWORK = list(get_args(DimensionInSkanRawFromNetwork))

def is_dimension_in_skan_raw_from_network(name: Union[str, DimensionInSkanRawFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkanRawFromNetwork` from Singular.
    """
    return name in DIMENSION_IN_SKAN_RAW_FROM_NETWORK


DimensionInSkanRawFromTracker = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
]

DimensionInSkanRawFromTrackerArgs = Union[Iterable[DimensionInSkanRawFromTracker], str]

DIMENSION_IN_SKAN_RAW_FROM_TRACKER = list(get_args(DimensionInSkanRawFromTracker))

def is_dimension_in_skan_raw_from_tracker(name: Union[str, DimensionInSkanRawFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInSkanRawFromTracker` from Singular.
    """
    return name in DIMENSION_IN_SKAN_RAW_FROM_TRACKER


DimensionInAdMon = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
]

DimensionInAdMonArgs = Union[Iterable[DimensionInAdMon], str]

DIMENSION_IN_AD_MON = list(get_args(DimensionInAdMon))

def is_dimension_in_ad_mon(name: Union[str, DimensionInAdMon]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInAdMon` from Singular.
    """
    return name in DIMENSION_IN_AD_MON


DimensionInAdMonFromNetwork = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
]

DimensionInAdMonFromNetworkArgs = Union[Iterable[DimensionInAdMonFromNetwork], str]

DIMENSION_IN_AD_MON_FROM_NETWORK = list(get_args(DimensionInAdMonFromNetwork))

def is_dimension_in_ad_mon_from_network(name: Union[str, DimensionInAdMonFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInAdMonFromNetwork` from Singular.
    """
    return name in DIMENSION_IN_AD_MON_FROM_NETWORK


DimensionInAdMonFromTracker = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
]

DimensionInAdMonFromTrackerArgs = Union[Iterable[DimensionInAdMonFromTracker], str]

DIMENSION_IN_AD_MON_FROM_TRACKER = list(get_args(DimensionInAdMonFromTracker))

def is_dimension_in_ad_mon_from_tracker(name: Union[str, DimensionInAdMonFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionInAdMonFromTracker` from Singular.
    """
    return name in DIMENSION_IN_AD_MON_FROM_TRACKER


DimensionFromNetwork = Literal[
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
    "original_metadata_currency",
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

DimensionFromNetworkArgs = Union[Iterable[DimensionFromNetwork], str]

DIMENSION_FROM_NETWORK = list(get_args(DimensionFromNetwork))

def is_dimension_from_network(name: Union[str, DimensionFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionFromNetwork` from Singular.
    """
    return name in DIMENSION_FROM_NETWORK


DimensionFromTracker = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "app",
    "site_public_id",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "city_field",
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
    "min_roas",
    "installer_source",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "creative_type",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "os",
    "platform",
    "region_field",
    "skan_redownloads",
    "retention",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "standardized_bid_strategy",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_creative_id",
    "tracker_creative_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
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

DimensionFromTrackerArgs = Union[Iterable[DimensionFromTracker], str]

DIMENSION_FROM_TRACKER = list(get_args(DimensionFromTracker))

def is_dimension_from_tracker(name: Union[str, DimensionFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `DimensionFromTracker` from Singular.
    """
    return name in DIMENSION_FROM_TRACKER


Metric = Literal[
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

MetricArgs = Union[Iterable[Metric], str]

METRIC = list(get_args(Metric))

def is_metric(name: Union[str, Metric]) -> bool:
    """
    Check if `name` is a valid non-custom `Metric` from Singular.
    """
    return name in METRIC


MetricInGeneral = Literal[
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

MetricInGeneralArgs = Union[Iterable[MetricInGeneral], str]

METRIC_IN_GENERAL = list(get_args(MetricInGeneral))

def is_metric_in_general(name: Union[str, MetricInGeneral]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInGeneral` from Singular.
    """
    return name in METRIC_IN_GENERAL


MetricInGeneralFromNetwork = Literal[
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

MetricInGeneralFromNetworkArgs = Union[Iterable[MetricInGeneralFromNetwork], str]

METRIC_IN_GENERAL_FROM_NETWORK = list(get_args(MetricInGeneralFromNetwork))

def is_metric_in_general_from_network(name: Union[str, MetricInGeneralFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInGeneralFromNetwork` from Singular.
    """
    return name in METRIC_IN_GENERAL_FROM_NETWORK


MetricInGeneralFromTracker = Literal[
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

MetricInGeneralFromTrackerArgs = Union[Iterable[MetricInGeneralFromTracker], str]

METRIC_IN_GENERAL_FROM_TRACKER = list(get_args(MetricInGeneralFromTracker))

def is_metric_in_general_from_tracker(name: Union[str, MetricInGeneralFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInGeneralFromTracker` from Singular.
    """
    return name in METRIC_IN_GENERAL_FROM_TRACKER


MetricInCreative = Literal[
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

MetricInCreativeArgs = Union[Iterable[MetricInCreative], str]

METRIC_IN_CREATIVE = list(get_args(MetricInCreative))

def is_metric_in_creative(name: Union[str, MetricInCreative]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInCreative` from Singular.
    """
    return name in METRIC_IN_CREATIVE


MetricInCreativeFromNetwork = Literal[
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

MetricInCreativeFromNetworkArgs = Union[Iterable[MetricInCreativeFromNetwork], str]

METRIC_IN_CREATIVE_FROM_NETWORK = list(get_args(MetricInCreativeFromNetwork))

def is_metric_in_creative_from_network(name: Union[str, MetricInCreativeFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInCreativeFromNetwork` from Singular.
    """
    return name in METRIC_IN_CREATIVE_FROM_NETWORK


MetricInCreativeFromTracker = Literal[
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

MetricInCreativeFromTrackerArgs = Union[Iterable[MetricInCreativeFromTracker], str]

METRIC_IN_CREATIVE_FROM_TRACKER = list(get_args(MetricInCreativeFromTracker))

def is_metric_in_creative_from_tracker(name: Union[str, MetricInCreativeFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInCreativeFromTracker` from Singular.
    """
    return name in METRIC_IN_CREATIVE_FROM_TRACKER


MetricInSkan = Literal[
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

MetricInSkanArgs = Union[Iterable[MetricInSkan], str]

METRIC_IN_SKAN = list(get_args(MetricInSkan))

def is_metric_in_skan(name: Union[str, MetricInSkan]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkan` from Singular.
    """
    return name in METRIC_IN_SKAN


MetricInSkanFromNetwork = Literal[
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

MetricInSkanFromNetworkArgs = Union[Iterable[MetricInSkanFromNetwork], str]

METRIC_IN_SKAN_FROM_NETWORK = list(get_args(MetricInSkanFromNetwork))

def is_metric_in_skan_from_network(name: Union[str, MetricInSkanFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkanFromNetwork` from Singular.
    """
    return name in METRIC_IN_SKAN_FROM_NETWORK


MetricInSkanFromTracker = Literal[
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

MetricInSkanFromTrackerArgs = Union[Iterable[MetricInSkanFromTracker], str]

METRIC_IN_SKAN_FROM_TRACKER = list(get_args(MetricInSkanFromTracker))

def is_metric_in_skan_from_tracker(name: Union[str, MetricInSkanFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkanFromTracker` from Singular.
    """
    return name in METRIC_IN_SKAN_FROM_TRACKER


MetricInSkanRaw = Literal[
    "skan_conversion_values_count",
    "skan_installs",
]

MetricInSkanRawArgs = Union[Iterable[MetricInSkanRaw], str]

METRIC_IN_SKAN_RAW = list(get_args(MetricInSkanRaw))

def is_metric_in_skan_raw(name: Union[str, MetricInSkanRaw]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkanRaw` from Singular.
    """
    return name in METRIC_IN_SKAN_RAW


MetricInSkanRawFromNetwork = Literal[
    "skan_conversion_values_count",
    "skan_installs",
]

MetricInSkanRawFromNetworkArgs = Union[Iterable[MetricInSkanRawFromNetwork], str]

METRIC_IN_SKAN_RAW_FROM_NETWORK = list(get_args(MetricInSkanRawFromNetwork))

def is_metric_in_skan_raw_from_network(name: Union[str, MetricInSkanRawFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkanRawFromNetwork` from Singular.
    """
    return name in METRIC_IN_SKAN_RAW_FROM_NETWORK


MetricInSkanRawFromTracker = Literal[
    "skan_conversion_values_count",
    "skan_installs",
]

MetricInSkanRawFromTrackerArgs = Union[Iterable[MetricInSkanRawFromTracker], str]

METRIC_IN_SKAN_RAW_FROM_TRACKER = list(get_args(MetricInSkanRawFromTracker))

def is_metric_in_skan_raw_from_tracker(name: Union[str, MetricInSkanRawFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInSkanRawFromTracker` from Singular.
    """
    return name in METRIC_IN_SKAN_RAW_FROM_TRACKER


MetricInAdMon = Literal[
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

MetricInAdMonArgs = Union[Iterable[MetricInAdMon], str]

METRIC_IN_AD_MON = list(get_args(MetricInAdMon))

def is_metric_in_ad_mon(name: Union[str, MetricInAdMon]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInAdMon` from Singular.
    """
    return name in METRIC_IN_AD_MON


MetricInAdMonFromNetwork = Literal[
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

MetricInAdMonFromNetworkArgs = Union[Iterable[MetricInAdMonFromNetwork], str]

METRIC_IN_AD_MON_FROM_NETWORK = list(get_args(MetricInAdMonFromNetwork))

def is_metric_in_ad_mon_from_network(name: Union[str, MetricInAdMonFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInAdMonFromNetwork` from Singular.
    """
    return name in METRIC_IN_AD_MON_FROM_NETWORK


MetricInAdMonFromTracker = Literal[
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

MetricInAdMonFromTrackerArgs = Union[Iterable[MetricInAdMonFromTracker], str]

METRIC_IN_AD_MON_FROM_TRACKER = list(get_args(MetricInAdMonFromTracker))

def is_metric_in_ad_mon_from_tracker(name: Union[str, MetricInAdMonFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricInAdMonFromTracker` from Singular.
    """
    return name in METRIC_IN_AD_MON_FROM_TRACKER


MetricFromNetwork = Literal[
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

MetricFromNetworkArgs = Union[Iterable[MetricFromNetwork], str]

METRIC_FROM_NETWORK = list(get_args(MetricFromNetwork))

def is_metric_from_network(name: Union[str, MetricFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricFromNetwork` from Singular.
    """
    return name in METRIC_FROM_NETWORK


MetricFromTracker = Literal[
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

MetricFromTrackerArgs = Union[Iterable[MetricFromTracker], str]

METRIC_FROM_TRACKER = list(get_args(MetricFromTracker))

def is_metric_from_tracker(name: Union[str, MetricFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `MetricFromTracker` from Singular.
    """
    return name in METRIC_FROM_TRACKER


FieldInGeneral = Literal[
    "adn_account_id",
    "adn_account_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
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
    "country_field",
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
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracking_url",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
    "adn_utc_offset",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

FieldInGeneralArgs = Union[Iterable[FieldInGeneral], str]

FIELD_IN_GENERAL = list(get_args(FieldInGeneral))

def is_field_in_general(name: Union[str, FieldInGeneral]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInGeneral` from Singular.
    """
    return name in FIELD_IN_GENERAL


FieldInGeneralFromNetwork = Literal[
    "adn_account_id",
    "adn_account_name",
    "affiliate_id",
    "affiliate_name",
    "app",
    "site_public_id",
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
    "country_field",
    "device_model",
    "dma_id_field",
    "dma_name_field",
    "fb_adset_id",
    "fb_campaign_id",
    "min_roas",
    "final_url",
    "is_uac",
    "keyword",
    "keyword_id",
    "keyword_match_type",
    "adn_campaign_id",
    "adn_campaign_name",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "adn_original_currency",
    "os",
    "placement",
    "platform",
    "publisher_id",
    "publisher_site_id",
    "publisher_site_name",
    "quality_score",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "standardized_bid_type",
    "adn_status",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracking_url",
    "adn_utc_offset",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

FieldInGeneralFromNetworkArgs = Union[Iterable[FieldInGeneralFromNetwork], str]

FIELD_IN_GENERAL_FROM_NETWORK = list(get_args(FieldInGeneralFromNetwork))

def is_field_in_general_from_network(name: Union[str, FieldInGeneralFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInGeneralFromNetwork` from Singular.
    """
    return name in FIELD_IN_GENERAL_FROM_NETWORK


FieldInGeneralFromTracker = Literal[
    "app",
    "site_public_id",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "city_field",
    "conversion_type",
    "country_field",
    "min_roas",
    "installer_source",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "os",
    "platform",
    "region_field",
    "retention",
    "source",
    "standardized_bid_strategy",
    "sub_campaign_id",
    "sub_campaign_name",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
    "admon_data_source",
    "data_connector_id",
    "data_connector_source_name",
    "data_connector_timestamp_utc",
    "data_connector_username",
    "singular_campaign_id",
    "frequency",
    "custom_clicks",
    "clicks_discrepancy",
    "adn_comments",
    "adn_cost",
    "daily_active_users",
    "adn_estimated_total_conversions",
    "custom_impressions",
    "impressions_discrepancy",
    "custom_installs",
    "installs_discrepancy",
    "adn_likes",
    "adn_clicks",
    "adn_impressions",
    "adn_installs",
    "adn_original_cost",
    "adn_original_currency",
    "original_revenue",
    "page_follows",
    "posts_saved",
    "tracker_reengagements",
    "reach",
    "revenue",
    "adn_shares",
    "tracker_clicks",
    "tracker_installs",
]

FieldInGeneralFromTrackerArgs = Union[Iterable[FieldInGeneralFromTracker], str]

FIELD_IN_GENERAL_FROM_TRACKER = list(get_args(FieldInGeneralFromTracker))

def is_field_in_general_from_tracker(name: Union[str, FieldInGeneralFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInGeneralFromTracker` from Singular.
    """
    return name in FIELD_IN_GENERAL_FROM_TRACKER


FieldInCreative = Literal[
    "adn_account_id",
    "adn_account_name",
    "app",
    "asset_id",
    "asset_name",
    "unified_campaign_id",
    "unified_campaign_name",
    "adn_campaign_url",
    "adn_click_type",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "adn_creative_id",
    "adn_creative_name",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_creative_id",
    "tracker_creative_name",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

FieldInCreativeArgs = Union[Iterable[FieldInCreative], str]

FIELD_IN_CREATIVE = list(get_args(FieldInCreative))

def is_field_in_creative(name: Union[str, FieldInCreative]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInCreative` from Singular.
    """
    return name in FIELD_IN_CREATIVE


FieldInCreativeFromNetwork = Literal[
    "adn_account_id",
    "adn_account_name",
    "app",
    "asset_id",
    "asset_name",
    "unified_campaign_id",
    "unified_campaign_name",
    "adn_campaign_url",
    "adn_click_type",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "adn_creative_id",
    "adn_creative_name",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "adn_subadnetwork",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

FieldInCreativeFromNetworkArgs = Union[Iterable[FieldInCreativeFromNetwork], str]

FIELD_IN_CREATIVE_FROM_NETWORK = list(get_args(FieldInCreativeFromNetwork))

def is_field_in_creative_from_network(name: Union[str, FieldInCreativeFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInCreativeFromNetwork` from Singular.
    """
    return name in FIELD_IN_CREATIVE_FROM_NETWORK


FieldInCreativeFromTracker = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "conversion_type",
    "country_field",
    "creative_format",
    "creative_height",
    "creative_id",
    "creative_name",
    "creative_reported_url",
    "creative_width",
    "creative_type",
    "os",
    "platform",
    "retention",
    "source",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_creative_id",
    "tracker_creative_name",
    "creative_hash",
    "creative_is_video",
    "creative_url",
    "creative_image_hash",
    "singular_creative_id",
    "completed_video_views",
    "video_views",
    "video_views_25pct",
    "video_views_50pct",
    "video_views_75pct",
]

FieldInCreativeFromTrackerArgs = Union[Iterable[FieldInCreativeFromTracker], str]

FIELD_IN_CREATIVE_FROM_TRACKER = list(get_args(FieldInCreativeFromTracker))

def is_field_in_creative_from_tracker(name: Union[str, FieldInCreativeFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInCreativeFromTracker` from Singular.
    """
    return name in FIELD_IN_CREATIVE_FROM_TRACKER


FieldInSkan = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

FieldInSkanArgs = Union[Iterable[FieldInSkan], str]

FIELD_IN_SKAN = list(get_args(FieldInSkan))

def is_field_in_skan(name: Union[str, FieldInSkan]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkan` from Singular.
    """
    return name in FIELD_IN_SKAN


FieldInSkanFromNetwork = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

FieldInSkanFromNetworkArgs = Union[Iterable[FieldInSkanFromNetwork], str]

FIELD_IN_SKAN_FROM_NETWORK = list(get_args(FieldInSkanFromNetwork))

def is_field_in_skan_from_network(name: Union[str, FieldInSkanFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkanFromNetwork` from Singular.
    """
    return name in FIELD_IN_SKAN_FROM_NETWORK


FieldInSkanFromTracker = Literal[
    "app",
    "unified_campaign_id",
    "unified_campaign_name",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_report_network_clicks",
    "skan_conversion_values_count",
    "adn_cost",
    "skan_estimated_revenue",
    "skan_estimated_ROI",
    "skan_report_network_impressions",
    "skan_installs",
    "skan_revenue",
    "skan_roi",
    "tracker_installs",
]

FieldInSkanFromTrackerArgs = Union[Iterable[FieldInSkanFromTracker], str]

FIELD_IN_SKAN_FROM_TRACKER = list(get_args(FieldInSkanFromTracker))

def is_field_in_skan_from_tracker(name: Union[str, FieldInSkanFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkanFromTracker` from Singular.
    """
    return name in FIELD_IN_SKAN_FROM_TRACKER


FieldInSkanRaw = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_conversion_values_count",
    "skan_installs",
]

FieldInSkanRawArgs = Union[Iterable[FieldInSkanRaw], str]

FIELD_IN_SKAN_RAW = list(get_args(FieldInSkanRaw))

def is_field_in_skan_raw(name: Union[str, FieldInSkanRaw]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkanRaw` from Singular.
    """
    return name in FIELD_IN_SKAN_RAW


FieldInSkanRawFromNetwork = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_conversion_values_count",
    "skan_installs",
]

FieldInSkanRawFromNetworkArgs = Union[Iterable[FieldInSkanRawFromNetwork], str]

FIELD_IN_SKAN_RAW_FROM_NETWORK = list(get_args(FieldInSkanRawFromNetwork))

def is_field_in_skan_raw_from_network(name: Union[str, FieldInSkanRawFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkanRawFromNetwork` from Singular.
    """
    return name in FIELD_IN_SKAN_RAW_FROM_NETWORK


FieldInSkanRawFromTracker = Literal[
    "app",
    "skan_conversion_value",
    "skan_conversion_value_description",
    "country_field",
    "skan_redownloads",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "skan_validated",
    "skan_conversion_values_count",
    "skan_installs",
]

FieldInSkanRawFromTrackerArgs = Union[Iterable[FieldInSkanRawFromTracker], str]

FIELD_IN_SKAN_RAW_FROM_TRACKER = list(get_args(FieldInSkanRawFromTracker))

def is_field_in_skan_raw_from_tracker(name: Union[str, FieldInSkanRawFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInSkanRawFromTracker` from Singular.
    """
    return name in FIELD_IN_SKAN_RAW_FROM_TRACKER


FieldInAdMon = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

FieldInAdMonArgs = Union[Iterable[FieldInAdMon], str]

FIELD_IN_AD_MON = list(get_args(FieldInAdMon))

def is_field_in_ad_mon(name: Union[str, FieldInAdMon]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInAdMon` from Singular.
    """
    return name in FIELD_IN_AD_MON


FieldInAdMonFromNetwork = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

FieldInAdMonFromNetworkArgs = Union[Iterable[FieldInAdMonFromNetwork], str]

FIELD_IN_AD_MON_FROM_NETWORK = list(get_args(FieldInAdMonFromNetwork))

def is_field_in_ad_mon_from_network(name: Union[str, FieldInAdMonFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInAdMonFromNetwork` from Singular.
    """
    return name in FIELD_IN_AD_MON_FROM_NETWORK


FieldInAdMonFromTracker = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "site_public_id",
    "ad_country",
    "ad_clicks",
    "ad_impressions",
    "ad_requests",
    "ad_revenue",
    "bid_requests",
    "bid_responses",
    "ad_completed_video_views",
    "filled_ad_requests",
    "total_revenue",
    "ad_video_views",
]

FieldInAdMonFromTrackerArgs = Union[Iterable[FieldInAdMonFromTracker], str]

FIELD_IN_AD_MON_FROM_TRACKER = list(get_args(FieldInAdMonFromTracker))

def is_field_in_ad_mon_from_tracker(name: Union[str, FieldInAdMonFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldInAdMonFromTracker` from Singular.
    """
    return name in FIELD_IN_AD_MON_FROM_TRACKER


FieldFromNetwork = Literal[
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
    "original_metadata_currency",
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

FieldFromNetworkArgs = Union[Iterable[FieldFromNetwork], str]

FIELD_FROM_NETWORK = list(get_args(FieldFromNetwork))

def is_field_from_network(name: Union[str, FieldFromNetwork]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldFromNetwork` from Singular.
    """
    return name in FIELD_FROM_NETWORK


FieldFromTracker = Literal[
    "instance_id",
    "instance_name",
    "source",
    "ad_placement_id",
    "ad_placement_name",
    "ad_type_id",
    "ad_type_name",
    "app",
    "site_public_id",
    "opt_in",
    "banner_name",
    "bid_amount",
    "bid_strategy",
    "bid_type",
    "unified_campaign_id",
    "unified_campaign_name",
    "campaign_objective",
    "campaign_status",
    "city_field",
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
    "min_roas",
    "installer_source",
    "adn_sub_campaign_id",
    "adn_sub_campaign_name",
    "creative_type",
    "install_app_store",
    "original_bid_amount",
    "original_metadata_currency",
    "os",
    "platform",
    "region_field",
    "skan_redownloads",
    "retention",
    "skan_app_id",
    "skan_campaign_id",
    "skan_network_id",
    "skan_publisher_id",
    "source",
    "standardized_bid_strategy",
    "sub_campaign_id",
    "sub_campaign_name",
    "creative_text",
    "tracker_campaign_id",
    "tracker_campaign_name",
    "tracker_creative_id",
    "tracker_creative_name",
    "tracker_name",
    "tracker_source_name",
    "tracker_sub_campaign_id",
    "tracker_sub_campaign_name",
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

FieldFromTrackerArgs = Union[Iterable[FieldFromTracker], str]

FIELD_FROM_TRACKER = list(get_args(FieldFromTracker))

def is_field_from_tracker(name: Union[str, FieldFromTracker]) -> bool:
    """
    Check if `name` is a valid non-custom `FieldFromTracker` from Singular.
    """
    return name in FIELD_FROM_TRACKER


FIELD_MAPPING = dict(
    adn_account_id="Account ID",
    adn_account_name="Account Name",
    instance_id="Ad Instance ID",
    instance_name="Ad Instance Name",
    source="Source",
    ad_placement_id="Ad PlacementPlacement: A field in Singular reporting that says where/when the ad was displayed in the website/app (the precise meaning varies between networks). Not to be confused with Ad Placement (which is an Ad Mon-specific dimension). ID",
    ad_placement_name="Ad Placement Name",
    ad_type_id="Ad Type ID",
    ad_type_name="Ad Type Name",
    affiliate_id="Affiliate ID",
    affiliate_name="Affiliate Name",
    app="App",
    site_public_id="App ID",
    asset_id="Asset ID",
    asset_name="Asset Name",
    opt_in="ATT opt in",
    banner_name="Banner Name",
    bid_amount="Bid Amount",
    bid_strategy="Bid Strategy",
    bid_type="Bid Type",
    unified_campaign_id="Campaign ID",
    unified_campaign_name="Campaign Name",
    campaign_objective="Campaign Objective",
    campaign_status="Campaign Status",
    adn_campaign_url="Campaign URL",
    city_field="City",
    adn_click_type="Click Type",
    conversion_type="Conversion Type",
    skan_conversion_value="Conversion ValueConversion Value: A single number between 0 and 63 included in an SKAdNetwork postback. The conversion value is the only way to get any information about an install and the user's post-install activity in the SKAdNetwork framework. Learn more",
    skan_conversion_value_description="Conversion Value Description",
    country_field="Country",
    ad_country="Country",
    creative_format="Creative Format",
    creative_height="Creative Height",
    creative_id="Creative ID",
    creative_name="Creative Name",
    creative_reported_url="Creative Reported URL",
    creative_width="Creative Width",
    device_model="Device Model",
    dma_id_field="DMA ID",
    dma_name_field="DMA Name",
    fb_adset_id="Facebook Ad Set ID",
    fb_campaign_id="Facebook Campaign ID",
    min_roas="Facebook ROAS Bid",
    final_url="Final URL",
    installer_source="Installer Source",
    is_uac="Is UAC",
    keyword="Keyword",
    keyword_id="Keyword ID",
    keyword_match_type="Keyword Match Type",
    adn_campaign_id="Network Campaign ID",
    adn_campaign_name="Network Campaign Name",
    adn_creative_id="Network Creative ID",
    adn_creative_name="Network Creative Name",
    adn_sub_campaign_id="Network Sub Campaign ID",
    adn_sub_campaign_name="Network Sub Campaign Name",
    creative_type="Normalized Creative Type",
    install_app_store="Normalized Installer Source",
    original_bid_amount="Original Bid Amount",
    original_metadata_currency="Original Bid Currency",
    adn_original_currency="Original Currency",
    os="OS",
    placement="Placement",
    platform="Platform",
    publisher_id="Publisher ID",
    publisher_site_id="Publisher Site ID",
    publisher_site_name="Publisher Site Name",
    quality_score="Quality ScoreQuality Score: A field in Singular reporting that contains the rating for the quality of ad content and landing pages, as compared to advertisers. Learn more in the Metrics and Dimensions Glossary",
    region_field="Region",
    skan_redownloads="Re-Downloads",
    retention="RetargetingRetargeting: A type of mobile marketing campaign that targets existing users of an app/website and aims to get them to re-engage with the product. Learn more",
    skan_app_id="SKANSKAN: Singular's SKAdNetwork solution, offering smart conversion value management that can be configured through the Singular app. Learn more  App ID",
    skan_campaign_id="SKAN Campaign ID",
    skan_network_id="SKAN Network ID",
    skan_publisher_id="SKAN Publisher ID",
    standardized_bid_strategy="Standardized Bid Strategy",
    standardized_bid_type="Standardized Bid Type",
    adn_status="Status",
    adn_subadnetwork="Sub Ad Network",
    sub_campaign_id="Sub Campaign ID",
    sub_campaign_name="Sub Campaign Name",
    creative_text="Text",
    tracking_url="Tracking URL",
    tracker_campaign_id="Tracker Campaign ID",
    tracker_campaign_name="Tracker Campaign Name",
    tracker_creative_id="Tracker Creative ID",
    tracker_creative_name="Tracker Creative Name",
    tracker_name="Tracker Name",
    tracker_source_name="Tracker Source Name",
    tracker_sub_campaign_id="Tracker Sub Campaign ID",
    tracker_sub_campaign_name="Tracker Sub Campaign Name",
    adn_utc_offset="UTC Offset",
    utm_campaign="UTM Campaign",
    utm_content="UTM Content",
    utm_medium="UTM Medium",
    utm_source="UTM Source",
    utm_term="UTM Term",
    skan_validated="Validated",
    admon_data_source="nan",
    creative_hash="nan",
    creative_is_video="nan",
    creative_url="nan",
    creative_image_hash="nan",
    data_connector_id="nan",
    data_connector_source_name="nan",
    data_connector_timestamp_utc="nan",
    data_connector_username="nan",
    singular_campaign_id="nan",
    singular_creative_id="nan",
    ad_clicks="Ad Clicks",
    ad_impressions="Ad Impressions",
    ad_requests="Ad Requests",
    ad_revenue="Ad Revenue",
    frequency="Average Frequency",
    bid_requests="Bid Requests",
    bid_responses="Bid Responses",
    custom_clicks="Clicks",
    skan_report_network_clicks="Clicks",
    clicks_discrepancy="Clicks Discrepancy",
    adn_comments="Comments",
    completed_video_views="Completed Video Views",
    ad_completed_video_views="Completed Video Views",
    skan_conversion_values_count="Conversion Values - Count",
    adn_cost="Cost",
    daily_active_users="DAU",
    adn_estimated_total_conversions="Est. Conversions",
    skan_estimated_revenue="Estimated Revenue",
    skan_estimated_ROI="Estimated ROI",
    filled_ad_requests="Filled Ad Requests",
    custom_impressions="Impressions",
    skan_report_network_impressions="Impressions",
    impressions_discrepancy="Impressions Discrepancy",
    custom_installs="Installs",
    installs_discrepancy="Installs Discrepancy",
    adn_likes="Likes",
    adn_clicks="Network Clicks",
    adn_impressions="Network Impressions",
    adn_installs="Network Installs",
    new_visitors="New Visitors",
    adn_original_cost="Original Cost",
    original_revenue="Original Revenue",
    page_follows="Page Follows",
    posts_saved="Posts saved",
    re_engaged_visitors="Re-engaged Visitors",
    tracker_reengagements="Re-Engagements",
    reach="Reach",
    revenue="Revenue",
    adn_shares="Shares",
    skan_installs="SKAN Installs",
    skan_revenue="SKAN Revenue",
    skan_roi="SKAN ROI",
    total_revenue="Total Revenue",
    total_web_conversions="Total Web Conversions",
    tracker_clicks="Tracker Clicks",
    tracker_installs="Tracker Installs",
    video_views="Video Views",
    ad_video_views="Video Views",
    video_views_25pct="Video Views 25%",
    video_views_50pct="Video Views 50%",
    video_views_75pct="Video Views 75%",
)


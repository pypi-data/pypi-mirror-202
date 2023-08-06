"""
Generates a python file that:
    Defines Literal types, constant lists, and validator function for all combinations
    of dimensions and metrics in Singular.

IMPORTANT:
    If Singular's master reference of dimensions and metrics changes, you can easily
    update the python type definitions (or get a csv of the new definitions) by following
    these 3 steps:
        1. Go to this link:  https://support.singular.net/hc/en-us/articles/203389179-Singular-Metrics-and-Dimensions-Descriptions
        2. Make sure the "Show:" filter is set to "All"
        4. Inspect element, copy TABLE's html (steps below), and either:
            a.) Paste into the _RAW_HTML variable below, and run this script.
            b.) Paste into a file, and run this script passing the file path as the `raw_html` argument.
        HOW TO COPY HTML TABLE
            1. Inspect element and hit the "Select an element" icon in upper left corner
            2. Click anywhere in table
            3. In raw html, starting from the highlighted line, look up until you see the opening <table> tag
            4. Right click and "Copy" -> "Copy outerHTML".
"""
from typing import List, overload, Literal, Iterable, Tuple, Optional, Union
import pandas as pd, numpy as np
import re
from singular_client.utils import (
    format_type,
    format_constant,
    format_variable,
)

DEFAULT_TABLE_FILENAME = "all_dimensions_and_metrics.csv"
DEFAULT_PY_MODULE_FILENAME = "dimensions_and_metrics.py"

REPORT_CATEGORIES = dict(
    in_general='general',
    in_creative='creative',
    in_skan='skan',
    in_skan_raw='skan raw',
    in_ad_mon='ad mon',
)
SOURCE_CATEGORIES = dict(
    from_network='network',
    from_tracker='tracker',
)

CATEGORIES = {**SOURCE_CATEGORIES, **REPORT_CATEGORIES}

class Naming:
    """ Naming options for generated python code. """
    # Type naming
    field_args = lambda x: x + "_args"  # "from_network_dimension" -> "from_network_dimension_args"
    validator_func = lambda x: "is_" + x  # "in_skan" -> def is_in_skan(x): ...
    constant_list = lambda x: x

def main(
    raw_html: Optional[str] = None,
    write_table: Union[str, bool] = True,
    write_py_module: Union[str, bool] = True,
) -> Tuple[pd.DataFrame, str]:
    """
    Returns tuple of:
        df: A pandas DataFrame with the processed data from html table
        code: A string of python code that defines stuff
    """

    # Use default html if none provided, or read file if text is short enough
    if not raw_html:
        raw_html = _RAW_HTML

    if len(raw_html) < 200:
        with open(raw_html, 'r') as f:
            raw_html = f.read()

    # Processing
    df = read_html(raw_html)
    code = generate_python_file(df.copy())

    # Writing
    if write_table:
        if write_table == True:
            write_table = DEFAULT_TABLE_FILENAME
        df.copy().to_csv(write_table, index=False)

    if write_py_module:
        if write_py_module == True:
            write_py_module = DEFAULT_PY_MODULE_FILENAME
        with open(write_py_module, 'w') as f:
            f.write(code)

    return df, code

def generate_python_file(df: pd.DataFrame) -> pd.DataFrame:

    df.dropna(subset=['name'], inplace=True)
    df['field'] = True
    df['dimension'] = np.where(df.kind == 'dimension', True, False)
    df['metric'] = np.where(df.kind == 'metric', True, False)

    def prefix(s, prefix=None):
        return f'{prefix}_{s}' if prefix else s

    s = DOC + IMPORTS

    base = "field"
    name = base
    s += generate_spec(name, df['name'])

    for field in ['dimension', 'metric']:
        df_field = df[df[field]]
        name_field = field
        s += generate_spec(name_field, df_field['name'])

        for report in REPORT_CATEGORIES:
            df_report = df_field[df_field[report]]
            name_report = prefix(report, name_field)
            s += generate_spec(name_report, df_report['name'])

            for source in SOURCE_CATEGORIES:
                df_source = df_report[df_report[source]]
                name_source = prefix(source, name_report)
                s += generate_spec(name_source, df_source['name'])

        for source in SOURCE_CATEGORIES:
            df_source = df_field[df_field[source]]
            name_source = prefix(source, name_field)
            s += generate_spec(name_source, df_source['name'])

    for report in REPORT_CATEGORIES:
        df_report = df[df[report]]
        name_report = prefix(report, base)
        s += generate_spec(name_report, df_report['name'])

        for source in SOURCE_CATEGORIES:
            df_source = df_report[df_report[source]]
            name_source = prefix(source, name_report)
            s += generate_spec(name_source, df_source['name'])

    for source in SOURCE_CATEGORIES:
        df_source = df[df[source]]
        name_source = prefix(source, base)
        s += generate_spec(name_source, df_source['name'])
    return s

def _list_value(value: str) -> str:
    return f'    "{value}",\n'

def _literal_type_name(name: str) -> str:
    return format_type(name)

def _constant_type_name(name: str) -> str:
    return format_constant(name)

def _args_type_name(name: str) -> str:
    return format_type(name) + "Args"

def _validator_func_name(name: str) -> str:
    return "is_" + format_variable(name)

def _gen_literal_type(name: str, values: Iterable[str]) -> str:
    """ Create Literal type using `values` as args"""
    type_name = _literal_type_name(name)
    s = type_name + " = Literal[\n"
    for value in values:
        s += _list_value(value)
    return s + "]\n\n"

def _gen_args_type(name: str) -> str:
    """
    Create a Union type that allows for an iterable of valid literals
    of a type, or a single string
    """
    type_name = _literal_type_name(name)
    args_name = _args_type_name(name)
    return f"{args_name} = Union[Iterable[{type_name}], str]\n\n"

def _gen_constant_list(name: str) -> str:
    """Extract args from Literal, `name`"""
    type_name = _literal_type_name(name)
    const_name = _constant_type_name(name)
    return f"{const_name} = list(get_args({type_name}))\n\n"

def _gen_validator_func_for_type(name: str) -> str:
    """Create validator function for type `name`"""
    constant_name = _constant_type_name(name)
    validator_name = _validator_func_name(name)
    type_name = _literal_type_name(name)
    return f'''def {validator_name}(name: Union[str, {type_name}]) -> bool:
    """
    Check if `name` is a valid non-custom `{type_name}` from Singular.
    """
    return name in {constant_name}


'''

def generate_spec(name: str, values: Iterable[str]) -> str:
    """Generate all 4 required items"""
    return (
        # _literal_type_name(name) + "\n"
        _gen_literal_type(name, values)
        + _gen_args_type(name)
        + _gen_constant_list(name)
        + _gen_validator_func_for_type(name)
    )

IMPORTS = "from typing import Literal, Iterable, Union, get_args\n\n\n"

DOC = '''"""
VALID PARAMETER TYPES FOR ENDPOINTS
===================================

Defines Literal types, constant lists, and validator function for all combinations
of dimensions and metrics in Singular.

Level 1
    Field
    Dimension
    Metric

Level 2
    InGeneral
    InCreative
    InSkan
    InSkan Raw
    InAd Mon
    
Level 3
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

'''


# ==============================================================================
# ==============================================================================
# HTML READING

def read_html(raw_html: Optional[str] = None) -> pd.DataFrame:
    """
    1. Go to this link: https://support.singular.net/hc/en-us/articles/203389179-Singular-Metrics-and-Dimensions-Descriptions
    2. Inspect element. Copy table HTML. Make sure "Show:" filter is set to "All"
    3. Paste the HTML into the _RAW_HTML variable below, and run this script.
    """
    if not raw_html:
        raw_html = _RAW_HTML
    dfs = pd.read_html(raw_html)
    assert len(dfs) >= 1, "No tables found in HTML"
    df = dfs[0]
    df = df.drop(0).reset_index(drop=True)

    df.columns = [
        'display_name',
        'name',
        'desc',
        'available_in',
        'pulled_from',
    ]

    def bool_if_contains(df, col, val) -> pd.Series:
        return np.where(
            df[col].str.lower().str.contains(val.lower()),
            True, False
        )

    # Separate data availability to boolean columns
    for new_name, name in SOURCE_CATEGORIES.items():
        df[new_name] = bool_if_contains(df, 'pulled_from', name)

    for new_name, name in REPORT_CATEGORIES.items():
        df[new_name] = bool_if_contains(df, 'available_in', name)

    # Fill nulls wil False
    for col in CATEGORIES:
        df.loc[:, col] = df[col].fillna(False).astype(bool)

    df.drop(
        columns=['pulled_from', 'available_in'],
        inplace=True
    )

    # Separate dimensions and metrics
    delimiter_index = df[df['display_name'] == 'Metrics'].index[0]
    df.insert(0, 'kind', 'dimension')
    df.loc[delimiter_index+1:, 'kind'] = 'metric'

    # Remove delimiter row
    df = df[df['display_name'] != 'Metrics']

    # Replace nulls with actual null
    df.replace(r"\bN/A\b", np.nan, regex=True, inplace=True)

    # Moving stuff around
    df.insert(len(df.columns)-1, 'desc', df.pop('desc'))
    df.reset_index(drop=True, inplace=True)
    df = df.copy()
    return df


_RAW_HTML = """
<table id="table1" class="table small-font" style="table-layout: fixed; width: 100%;">
<tbody>
<tr class="always-visible">
<th style="width: 12%;">Field Name in Web App</th>
<th style="width: 18%;">Field Name in API &amp; ETL</th>
<th style="width: 43%;">Description</th>
<th style="width: 15%;">Available in Reports<span style="font-weight: 400;"><br></span></th>
<th style="width: 12%;">Pulled From<br><span style="font-weight: 400;">(<a href="https://support.singular.net/hc/en-us/articles/205046069#which_metrics_network_tracker">Learn More</a>)</span></th>
</tr>
<tr class="always-visible">
<td style="background-color: #3089f4; width: 15%;" colspan="5">
<h2 style="color: #ffffff; font-size: large; font-weight: bold; margin: 0;">Dimensions</h2>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Account ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_account_</strong><strong>id</strong></div>
</td>
<td style="width: 43%;">
<div>Your account ID from which we pulled the data. In some networks, such as Facebook and Google Ads, you may have multiple ad account IDs.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Account Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_account_name</strong></div>
</td>
<td style="width: 43%;">
<div>The account name of the campaign, as reported by the ad network (when applicable).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Instance ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>instance_id</strong></div>
</td>
<td style="width: 43%;">
<div>The targeting (be it country or a specific app) associated with the bid. Some networks refer to this dimension as <strong>Line Item</strong> or <strong>Mediation Group</strong>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Instance Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>instance_name</strong></div>
</td>
<td style="width: 43%;">
<div>The targeting (be it country or a specific app) associated with the bid. Some networks refer to this dimension as <strong>Line Item</strong> or <strong>Mediation Group</strong>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong><span class="wysiwyg-underline"><span class="term">Ad Monetization<span class="definition definition-hidden"><strong>Ad Monetization</strong>: Earning revenue by showing ads in your mobile app. Singular can track ad revenue as well as in-app purchase revenue to give you your complete campaign ROI. <a href="https://support.singular.net/hc/en-us/articles/360022067552" target="_blank" rel="noopener">Learn more</a>
</span></span></span> <span class="wysiwyg-underline"><span class="term">Source<span class="definition definition-hidden"><strong>Source</strong>: In Singular reporting, a source is an ad network or other third-party platform in which you advertised your product.</span></span></span></strong></div>
</td>
<td style="width: 15%;">
<div><strong>source</strong></div>
</td>
<td style="width: 43%;">
<div>In Ad Monetization Reporting: the name of the monetization network.</div>
</td>
<td style="width: 15%;">
<div><br>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad <span class="wysiwyg-underline"><span class="term">Placement<span class="definition definition-hidden"><strong>Placement</strong>: A field in Singular reporting that says where/when the ad was displayed in the website/app (the precise meaning varies between networks). Not to be confused with <strong>Ad Placement </strong>(which is an Ad Mon-specific dimension).</span></span></span> ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_placement_id</strong></div>
</td>
<td style="width: 43%;">
<div>The placement of the ad within the app (not to be confused with the ad type or the geo). Note that this dimension is given different names in different ad networks.</div>
</td>
<td style="width: 15%;">
<div>
<p>&nbsp;</p>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Placement Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_placement_name</strong></div>
</td>
<td style="width: 43%;">
<div>The placement of the ad within the app (not to be confused with the ad type or the geo). Note that this dimension is given different names in different ad networks.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Type ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_type_id</strong></div>
</td>
<td style="width: 43%;">
<div>The type of the ad, e.g., "banner" or "rewarded video". In other platforms, this may be referred to as the <strong>Ad Unit</strong> or the <strong>Ad Format</strong>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Type Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_type_name</strong></div>
</td>
<td style="width: 43%;">
<div>The type of the ad, e.g., "banner" or "rewarded video". In other platforms, this may be referred to as the <strong>Ad Unit</strong> or the <strong>Ad Format</strong>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Affiliate ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>affiliate_id</strong></div>
</td>
<td style="width: 43%;">
<div>In cases where there is a third party involved in the campaign, e.g. if the network bought inventory from another platform, or a DSP bought inventory from an exchange, this is the ID of the platform/exchange.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Affiliate Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>affiliate_name</strong></div>
</td>
<td style="width: 43%;">
<div>In cases where there is a third party involved in the campaign, e.g. if the network bought inventory from another platform, or a DSP bought inventory from an exchange, this is the name of the platform/exchange.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>App</strong></div>
</td>
<td style="width: 15%;">
<div><strong>app</strong></div>
</td>
<td style="width: 43%;">
<div>The app name as configured in the <strong>Apps </strong>page.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>App ID<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>site_public_id</strong></div>
</td>
<td style="width: 43%;">
<div>For apps, this is the app's ID in the Apple App Store or Google Play (see <a href="https://support.singular.net/hc/en-us/articles/360025661232-App-Configuration-FAQ?navigation_side_bar=true#h_5303a62d-7ab3-46bd-b1fb-f498722943c6">What is the difference between an app and an app site?</a>). For websites, this is the website URL.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Asset ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>asset_id</strong></div>
</td>
<td style="width: 43%;">
<div>"Asset ID" and "Asset Name" apply only to Google Ads UAC (mobile app) campaigns and Facebook Ads AAA campaigns. These campaigns have an additional level of granularity in which a single creative (ad) can contain multiple assets (images, videos, and texts), and each asset has its own name and ID. For more information, see the <a href="https://support.singular.net/hc/en-us/articles/360036750251-AdWords-Google-Ads-Data-Connector">Google Ads Data Connector Guide</a> and <a href="https://support.singular.net/hc/en-us/articles/208690176">Facebook Data Connector</a>.<br>Note: Due to a Google Ads API limitation, you currently can't see Installs broken down by asset, only by creative.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Asset Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>asset_name</strong></div>
</td>
<td style="width: 43%;">
<div>"Asset ID" and "Asset Name" apply only to Google Ads UAC (mobile app) campaigns and Facebook Ads AAA campaigns. These campaigns have an additional level of granularity in which a single creative (ad) can contain multiple assets (images, videos, and texts), and each asset has its own name and ID. For more information, see the <a href="https://support.singular.net/hc/en-us/articles/360036750251-AdWords-Google-Ads-Data-Connector">Google Ads Data Connector Guide</a> and <a href="https://support.singular.net/hc/en-us/articles/208690176">Facebook Data Connector</a>.<br>Note: Due to a Google Ads API limitation, you currently can't see Installs broken down by asset, only by creative.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>ATT opt in<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>opt_in<br></strong></div>
</td>
<td style="width: 43%;">
<div>A campaign and sub-campaign level dimension that indicates whether the user has consented to Apple's app transparency tracking. This dimension's values are "true" and "false". When we can't determine the value, it defaults to "false".</div>
<div><strong>Important:</strong> when using this dimension, you will not be able to see cost data.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Banner Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>banner_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the banner that the user clicked before they installed the app. This dimension is only available to <strong>Banners</strong> customers.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">Tracker</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Bid Amount</strong></div>
</td>
<td style="width: 15%;">
<div><strong>bid_amount</strong></div>
</td>
<td style="width: 43%;">
<div>The bid amount in your organization's default currency (converted from <strong>Original Bid Amount</strong>). Note: For Google Ads, Singular only pulls the bid amount for campaigns in which the <strong>Bid Type</strong> is “Target CPA”.<br><br>See the <a href="https://support.singular.net/hc/en-us/articles/360032548672-Campaign-Properties-FAQ">Campaign Properties FAQ</a> for more information.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Bid Strategy</strong></div>
</td>
<td style="width: 15%;">
<div><strong>bid_strategy</strong></div>
</td>
<td style="width: 43%;">
<div>This dimension contains the original data that we pulled from the ad network in order to deduce the <strong>Standardized Bid Strategy</strong>.<br><br>See the <a href="https://support.singular.net/hc/en-us/articles/360032548672-Campaign-Properties-FAQ">Campaign Properties FAQ</a> for more information. To see exactly which setting we pull from each network and the logic we use to standardize it, see <a href="https://support.singular.net/hc/en-us/articles/360029409512" data-ol-has-click-handler="">Campaign Properties Data Mapping</a>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Bid Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>bid_type</strong></div>
</td>
<td style="width: 43%;">
<div>This dimension contains the original data that we pulled from the ad network in order to deduce the <strong>Standardized Bid Type</strong>.<br><br>See the <a href="https://support.singular.net/hc/en-us/articles/360032548672-Campaign-Properties-FAQ">Campaign Properties FAQ</a> for more information. To see exactly which setting we pull from each network and the logic we use to standardize it, see <a href="https://support.singular.net/hc/en-us/articles/360029409512" data-ol-has-click-handler="">Campaign Properties Data Mapping</a>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>unified_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the campaign (see <strong>Campaign Name</strong> for more information).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>unified_campaign_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the campaign. Usually this is pulled from the ad network, but if it's missing in the ad network, the dimension reflects the campaign name reported by the attribution tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Campaign Objective</strong></div>
</td>
<td style="width: 15%;">
<div><strong>campaign_objective</strong></div>
</td>
<td style="width: 43%;">
<div>For ad networks that distinguish between the campaign objective and the bid type, such as Facebook and Snapchat, this dimension contains the campaign objective. You can also use it to find out if this is a mobile app install campaign. To see exactly which setting we pull from each network to populate this dimension, see <a href="https://support.singular.net/hc/en-us/articles/360029409512" data-ol-has-click-handler="">Campaign Properties Data Mapping</a>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Campaign Status</strong></div>
</td>
<td style="width: 15%;">
<div><strong>campaign_status</strong></div>
</td>
<td style="width: 43%;">
<div>Is the campaign live or not? Note that this is not a standardized dimension, so it may contain different values based on the ad network, e.g. “live/not live” vs. “true/false”.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Campaign URL</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_campaign_url</strong></div>
</td>
<td style="width: 43%;">
<div>The URL that is triggered when a user clicks on a campaign ad (the tracking link URL), as reported by the network. See also: <strong>Final URL</strong>.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>City</strong></div>
</td>
<td style="width: 15%;">
<div><strong>city_field</strong></div>
</td>
<td style="width: 43%;">
<div>The user's city, as reported by the tracker, or else by certain ad networks. Not available for creative reports.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Click Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_click_type</strong></div>
</td>
<td style="width: 43%;">
<div>The click type as reported by the ad network, where applicable.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Conversion Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>conversion_type</strong></div>
</td>
<td style="width: 43%;">
<div>How the user interacted with the ad. Possible values: "Click-through" (an ad click) or "View-through" (an ad impression).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong><span class="wysiwyg-underline"><span class="term">Conversion Value<span class="definition definition-hidden"><strong>Conversion Value</strong>: A single number between 0 and 63 included in an <span class="wysiwyg-underline">SKAdNetwork</span> postback. The conversion value is the only way to get any information about an install and the user's post-install activity in the SKAdNetwork framework. <a href="https://support.singular.net/hc/en-us/articles/360051200231-Understanding-Singular-s-Conversion-Value-Management" target="_blank" rel="noopener">Learn more</a>
</span></span></span></strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_conversion_value</strong></div>
</td>
<td style="width: 43%;">
<div>The SKAdNetwork conversion value (a number between 0 and 63).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Conversion Value Description</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_conversion_value_description</strong></div>
</td>
<td style="width: 43%;">
<div>A summary of the meaning of the conversion value in the context of the conversion model defined for the campaign.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Country</strong></div>
</td>
<td style="width: 15%;">
<div><strong>country_field</strong></div>
</td>
<td style="width: 43%;">
<div>The user's country, as reported by the network or derived from the network's targeting settings. For example, in SKAdNetwork, the user's country is not provided, but sometimes Singular can fill in that information by looking at the network's targeting settings and seeing that the campaign was targeted to one country only.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Country</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_country</strong></div>
</td>
<td style="width: 43%;">
<div>The country in which the ad was served.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative Format</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_format</strong></div>
</td>
<td style="width: 43%;">
<div>The format of the creative as defined by the ad network. This dimension gives more detailed information than <strong>Normalized Creative Type</strong>. Currently available for Vungle, AppLovin, Unity, and IronSource campaigns.<br><br>The expected values are:<br><strong>For Vungle:</strong> "dynamic interstitial", "square dynamic interstitial", "showcase", "looping", "carousel", "gradient", "swipe"<br><strong>For AppLovin:</strong> "GRAPHIC", "VIDEO", "REWARD" (rewarded video), "PLAY" (playable ad)<br><strong>For Ironsource:</strong> “Video &amp; Carousel”, “Video &amp; Full Screen”, “Video &amp; Interactive End Card”, “Playable”, “Interactive Video”</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative Height</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_height</strong></div>
</td>
<td style="width: 43%;">
<div>The height of an image/video creative, in pixels.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_id</strong></div>
</td>
<td style="width: 43%;">
<div>The unique identifier of the creative.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the creative, usually given by the customer.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative Reported URL </strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_reported_url</strong></div>
</td>
<td style="width: 43%;">
<div>The URL that is triggered when the user clicks the creative.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Creative Width</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_width</strong></div>
</td>
<td style="width: 43%;">
<div>The width of an image/video creative, in pixels.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Device Model</strong></div>
</td>
<td style="width: 15%;">
<div><strong>device_model</strong></div>
</td>
<td style="width: 43%;">
<div>In Aura campaigns only: the device model the ad was displayed in, e.g., LM-X320.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>DMA ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>dma_id_field</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the Designated Marketing Area that the ad was targeted to. The availability of this dimension depends on the network. Not available for creative reports.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>DMA Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>dma_name_field</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the Designated Marketing Area that the ad was targeted to. The availability of this dimension depends on the network. Not available for creative reports.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Facebook Ad Set ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>fb_adset_id</strong></div>
</td>
<td style="width: 43%;">
<div>In Facebook campaigns only: the "Ad Set ID" given by Facebook.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Facebook Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>fb_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>In Facebook campaigns only: the campaign ID given by Facebook.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Facebook ROAS Bid</strong></div>
</td>
<td style="width: 15%;">
<div><strong>min_roas</strong></div>
</td>
<td style="width: 43%;">
<div>For Facebook campaigns in which the campaign objective was set to Lowest Cost with Min ROAS (rather than having a set bid amount in dollars), we store the minimum ROAS percent in this dimension. The <strong>Bid Amount</strong> dimension for these campaigns will be empty.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Final URL</strong></div>
</td>
<td style="width: 15%;">
<div><strong>final_url</strong></div>
</td>
<td style="width: 43%;">
<div>In Google Ads (AdWords) campaigns, this field contains the tracking link arguments (suffixes), as they are not included in the Campaign URL reported by Google.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Installer Source<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>installer_source<br></strong></div>
</td>
<td style="width: 43%;">
<div>The raw value of the package or applications that installed the app.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Is UAC</strong></div>
</td>
<td style="width: 15%;">
<div><strong>is_uac</strong></div>
</td>
<td style="width: 43%;">
<div>In Google Ads (AdWords) campaigns only: is the campaign a "Universal App Campaign" (<a href="https://support.google.com/google-ads/answer/6247380?hl=en">see Google's documentation for more information</a>).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Keyword</strong></div>
</td>
<td style="width: 15%;">
<div><strong>keyword</strong></div>
</td>
<td style="width: 43%;">
<div>In search results ad campaigns: the search keyword as reported by the ad network. Applicable to Apple Search Ads, Bing, Google Ads (AdWords), Yahoo, etc.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Keyword ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>keyword_id</strong></div>
</td>
<td style="width: 43%;">
<div>The internal ID given by the ad network to the targeted search keyword.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Keyword Match Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>keyword_match_type</strong></div>
</td>
<td style="width: 43%;">
<div>The matching strategy for search keywords, such as "broad" or "exact" phrase</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the campaign, as pulled from the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_campaign_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the campaign, as pulled from the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Network Creative ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_creative_id</strong></div>
</td>
<td style="width: 43%;">
<div>The creative ID as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Network Creative Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_creative_name</strong></div>
</td>
<td style="width: 43%;">
<div>The creative name as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Sub Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_sub_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the sub-campaign, as pulled from the ad network. A sub-campaign is Singular's name for an additional grouping of ads that some networks have under the campaign level. Some networks may call it "ad group" or "ad set".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Sub Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_sub_campaign_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the sub-campaign, as pulled from the ad network. A sub-campaign is Singular's name for an additional grouping of ads that some networks have under the campaign level. Some networks may call it "ad group" or "ad set".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Normalized Creative Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_type</strong></div>
</td>
<td style="width: 43%;">See the <strong>Creative Format</strong> dimension.<br><br><strong>Notes:</strong><br>This dimension was formerly named "Creative Type" in the web UI.</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Normalized Installer Source<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>install_app_store<br></strong></div>
</td>
<td style="width: 43%;">Names of the app store and applications that installed the app, i.e. iOS App Store, Google Play, Samsung Galaxy Store, Xiaomi, Huawei, etc.<br><em>Derived and standardized from the 'Install Source' dimension.</em></td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Bid Amount</strong></div>
</td>
<td style="width: 15%;">
<div><strong>original_bid_amount</strong></div>
</td>
<td style="width: 43%;">
<div>The bid amount in the original currency.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Bid Currency</strong></div>
</td>
<td style="width: 15%;">
<div><strong>original_ metadata_currency</strong></div>
</td>
<td style="width: 43%;">
<div>The original currency of the bid (see <strong>Original Bid Amount</strong>).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Currency</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_original_currency</strong></div>
</td>
<td style="width: 43%;">
<div>The original currency as reported by the ad network. This may be different from the default currency set up for you in Singular.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>OS</strong></div>
</td>
<td style="width: 15%;">
<div><strong>os</strong></div>
</td>
<td style="width: 43%;">
<div>The operating system of the marketed product. For an app, this usually indicates which app store the app is sold in, e.g., "iOS" or "Android".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Placement</strong></div>
</td>
<td style="width: 15%;">
<div><strong>placement</strong></div>
</td>
<td style="width: 43%;">
<div id="placement_dimension" style="float: right; margin-left: 20px;"><a style="font-size: small;" href="#placement_dimension">#</a></div>
<p>Where or when the ad is displayed in the website or app (the precise meaning varies between networks). Currently available for Facebook, Twitter, and Snapchat. Not to be confused with <strong>Ad Placement</strong>, which is an Ad Mon-specific dimension.<br><br><strong>Note:</strong> This network-only dimension will cause <a href="https://support.singular.net/hc/en-us/articles/360056059811-Understanding-Singular-Reporting-Data#<span class=">Joining_Network_and_Tracker_Data" target="_self"&gt;network data and tracker data to appear in separate rows</a>.<br><br></p>
<div class="accordion accordion--colored">
<div id="anchor1" class="accordion__item">
<div class="accordion__item-title small-font">The value of <strong>Placement</strong> is mapped from different networks as follows:</div>
<div class="accordion__item-content"><strong>Facebook:</strong><br><strong>• Field:</strong> device_platforms/ publisher_platforms/ facebook_positions/ instagram_positions/ audience_network_positions/ messenger_positions<br><strong>• Possible values:</strong> mobile, desktop, facebook, instagram, messenger, audience_network, feed, right_hand_column, instant_article, marketplace, video_feeds, search stream, story, explore, classic, instream_video, rewarded_video, messenger_home, sponsored_messages<br><br><strong>Twitter:</strong><br><strong>• Field:</strong> placements<br><strong>• Possible values:</strong> ALL_ON_TWITTER, PUBLISHER_NETWORK, TWITTER_PROFILE, TWITTER_SEARCH, TWITTER_TIMELINE, TAP_BANNER, TAP_FULL, TAP_FULL_LANDSCAPE, TAP_NATIVE, TAP_MRECT<br><br><strong>Snapchat:</strong><br><strong>• Field:</strong> snapchat_positions (placement_v2)<br><strong>• Possible values:</strong> INTERSTITIAL_USER, INTERSTITIAL_CONTENT, INSTREAM, FEED, CAMERA, GAMES, AUDIENCE_EXTENSION</div>
</div>
</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Platform</strong></div>
</td>
<td style="width: 15%;">
<div><strong>platform</strong></div>
</td>
<td style="width: 43%;">
<div>The platform of the marketed product, e.g., "iPhone" or "iPad".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Publisher ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>publisher_id</strong></div>
</td>
<td style="width: 43%;">
<div>The hashed ID of the publisher (app) in which the ad has been displayed.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Publisher Site ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>publisher_site_id</strong></div>
</td>
<td style="width: 43%;">
<div>The public ID of the publisher (app) in which the ad has been displayed. This field is only populated if this information is provided by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Publisher Site Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>publisher_site_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the publisher (app) in which the ad has been displayed. This field is only populated if this information is provided by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong><span class="wysiwyg-underline"><span class="term">Quality Score<span class="definition definition-hidden"><strong>Quality Score</strong>: A field in Singular reporting that contains the rating for the quality of ad content and landing pages, as compared to advertisers. <a href="https://support.singular.net/hc/en-us/articles/203389179-Singular-Metrics-and-Dimensions-Glossary" target="_self">Learn more in the Metrics and Dimensions Glossary</a>
</span></span></span></strong></div>
</td>
<td style="width: 15%;">
<div><strong>quality_score</strong></div>
</td>
<td style="width: 43%;">A rating for the relevance of ad content, and landing pages, provided by <strong>Google Ads (AdWords)</strong> and <strong>Bing</strong>. The value is 1-10 with 10 being the best score.&nbsp;<br><br>The higher the quality, the more relevant and useful the ad/landing page is to someone searching for that keyword, compared to other advertisers.<br><br>See also:<br><a href="https://support.google.com/google-ads/answer/6167118?hl=en" target="_self">Google Ads Help: About Quality Score</a><br><a href="http://help.ads.microsoft.com/#apex/ads/en/50894/-1" target="_self">Microsoft: Quality Score - Definition</a><br><a href="http://help.ads.microsoft.com/#apex/ads/en/50813/2" target="_self">Microsoft: Quality Score and Quality Impact in Depth</a><br><br><strong>Note:</strong> This network-only dimension will cause <a href="https://support.singular.net/hc/en-us/articles/360056059811-Understanding-Singular-Reporting-Data#Joining_Network_and_Tracker_Data" target="_self">network data and tracker data to appear in separate rows</a>.</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Region</strong></div>
</td>
<td style="width: 15%;">
<div><strong>region_field</strong></div>
</td>
<td style="width: 43%;">
<div>The user's geographic region, as reported by the tracker, or else by certain ad networks. Not available for creative reports.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Re-Downloads</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_redownloads</strong></div>
</td>
<td style="width: 43%;">
<div>Apple's SKAdNetwork postbacks include a "redownload" field. According to Apple, this is set to true if the app has already been downloaded and installed by the same user (same Apple ID). Singular marks every SKAdNetwork install accordingly as either a "download" or a "redownload."</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong><span class="wysiwyg-underline"><span class="term">Retargeting<span class="definition definition-hidden"><strong>Retargeting</strong>: 
<span>A type of mobile marketing campaign that targets existing users of an app/website and aims to get them to re-engage with the product</span>. <a href="https://support.singular.net/hc/en-us/articles/360044494651#what_is_retargeting" target="_blank" rel="noopener">Learn more</a>
</span></span></span></strong></div>
</td>
<td style="width: 15%;">
<div><strong>retention</strong></div>
</td>
<td style="width: 43%;">
<div>Whether the campaign is a retargeting campaign (Yes/No).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong><span class="wysiwyg-underline"><span class="term">SKAN<span class="definition definition-hidden"><strong>SKAN</strong>: Singular's SKAdNetwork solution, offering smart conversion value management that can be configured through the Singular app. <a href="https://support.singular.net/hc/en-us/articles/360051200231" target="_self">Learn more</a>
</span></span></span> App ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_app_id</strong></div>
</td>
<td style="width: 43%;">
<div>The value of the 'app-id' parameter in Apple's SKAdNetwork postback.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_campaign_id </strong></div>
</td>
<td style="width: 43%;">
<div>The value of the 'campaign-id' parameter in Apple's SKAdNetwork postback.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN Network ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_network_id </strong></div>
</td>
<td style="width: 43%;">
<div>The value of the 'ad-network-id' parameter in Apple's SKAdNetwork postback.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN Publisher ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_publisher_id</strong></div>
</td>
<td style="width: 43%;">
<div>The value of the 'source-app-id' parameter in Apple's SKAdNetwork postback.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Source</strong></div>
</td>
<td style="width: 15%;">
<div><strong>source</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the data source (usually the ad network).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Standardized Bid Strategy</strong></div>
</td>
<td style="width: 15%;">
<div><strong>standardized_bid_strategy</strong></div>
</td>
<td style="width: 43%;">
<div>The bid strategy for the campaign:<br><br><strong>Manual: </strong>A fixed bid you determined in advance, e.g. $7 per install or $8 per action.<br><strong>Target:</strong> Bidding based on a target bid amount, e.g. $7 CPI, as used in Facebook and Google Ads.<br><strong>Max: </strong>Bidding based on a maximum bid amount (e.g. in Facebook when your choice is “Lowest Cost with Bid Cap”). If this is your Standardized Bid Strategy, the Bid Amount represents the maximum amount you were willing to pay.<br><strong>Auto:</strong> Automatic bidding (e.g. in Facebook when your choice is “Lowest Cost without Cap”). If the Standardized Bid Strategy is Auto, the Bid Amount dimension is going to be empty.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Standardized Bid Type</strong></div>
</td>
<td style="width: 15%;">
<div><strong>standardized_bid_type</strong></div>
</td>
<td style="width: 43%;">
<div>The method by which the bid is set up: ROI (ROAS), CPM, CPC, CPI, CPA, or CPCV.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-campaign-properties" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Status</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_status</strong></div>
</td>
<td style="width: 43%;">
<div>The campaign status (enabled/disabled) as reported by the network (when applicable).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Sub Ad Network</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_subadnetwork</strong></div>
</td>
<td style="width: 43%;">
<div>The sub ad network, as reported by the ad network. This is an additional level of hierarchy that some networks have. E.g., Google Ads has YouTube, Shopping, etc.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Sub Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>sub_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The sub-campaign ID (when applicable). A sub-campaign is Singular's name for an additional grouping of ads that some networks have under the campaign level. Some networks may call it "ad group" or "ad set".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Sub Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>sub_campaign_name</strong></div>
</td>
<td style="width: 43%;">
<div>The sub-campaign name (when applicable). A sub-campaign is Singular's name for an additional grouping of ads that some networks have under the campaign level. Some networks may call it "ad group" or "ad set".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network/ Tracker</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Text</strong></div>
</td>
<td style="width: 15%;">
<div><strong>creative_text</strong></div>
</td>
<td style="width: 43%;">
<div>The text associated with the creative (the creative may or may not have other elements associated with it, such as an image or a video).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracking URL</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracking_url</strong></div>
</td>
<td style="width: 43%;">
<div>In Google Ads (AdWords) campaigns, each ad click triggers two separate URLs: a destination (e.g. the advertiser's store) and a tracking URL. This field contains the tracking URL.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The campaign ID as pulled from the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_campaign_name</strong></div>
</td>
<td style="width: 43%;">
<div>The campaign name as pulled from the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Tracker Creative ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_creative_id</strong></div>
</td>
<td style="width: 43%;">
<div>The creative ID as reported by the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Tracker Creative Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_creative_name</strong></div>
</td>
<td style="width: 43%;">
<div>The creative name as reported by the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name configured in the attribution tracker's platform for the tracking link.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Source Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_source_name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the ad network, as pulled from the tracker. May be slightly different than the <strong>Source</strong> field (which holds the network name as it's listed in Singular).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Sub Campaign ID</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_sub_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the sub campaign (ad group/ad set), as pulled from the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Sub Campaign Name</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_sub_campaign_ name</strong></div>
</td>
<td style="width: 43%;">
<div>The name of the sub campaign (ad group/ad set), as pulled from the tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Tracker</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>UTC Offset</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_utc_offset</strong></div>
</td>
<td style="width: 43%;">
<div>The timezone offset of the campaign data, relative to UTC.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>Network</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>UTM Campaign</strong></div>
</td>
<td style="width: 15%;">
<div><strong>utm_campaign</strong></div>
</td>
<td style="width: 43%;">
<div>A specific product promotion or strategic campaign.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>UTM Content</strong></div>
</td>
<td style="width: 15%;">
<div><strong>utm_content</strong></div>
</td>
<td style="width: 43%;">
<div><span>The specific target clicked to bring the user to the site, such as text link or banner ad.</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>UTM Medium</strong></div>
</td>
<td style="width: 15%;">
<div><strong>utm_medium</strong></div>
</td>
<td style="width: 43%;">
<div><span>The type of link used, such as CPC or email.</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>UTM Source</strong></div>
</td>
<td style="width: 15%;">
<div><strong>utm_source</strong></div>
</td>
<td style="width: 43%;"><span>The site that sent the traffic.</span></td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>UTM Term</strong></div>
</td>
<td style="width: 15%;">
<div><strong>utm_term</strong></div>
</td>
<td style="width: 43%;">
<div>Search terms used to find the site.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Validated</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_validated</strong></div>
</td>
<td style="width: 43%;">
<div>As a part of Singular's SKAdNetwork solution, Singular not only receives and parses SKAdNetwork postbacks from ad networks but also checks with Apple to confirm that each postback represents an actual install. Validation ensures that installs are not fraudulent.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>admon_data_source</strong></div>
</td>
<td style="width: 43%;">
<div>The source of data for ad revenue. This dimension is useful if you are using more than one method of pulling ad revenue ROI data (<a href="https://support.singular.net/hc/en-us/articles/360037411471-Setting-Up-User-Level-Revenue-Reporting">learn about the available methods</a>) and want to get the metrics broken down by source.<br><br><strong>Notes:</strong><br>-&nbsp; To get the name of the ad revenue metric, query the <a href="https://support.singular.net/hc/en-us/articles/360045245692-Reporting-API-Reference#<span class=">Cohort_Metrics_Endpoint"&gt;Cohort Metrics endpoint</a>.<br>- admon_data_source is only available in the API. If you are running reports in the Singular web app, see <a href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ#admon_transparency">How can I tell where my ad revenue data is taken from?</a></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>creative_hash</strong></div>
</td>
<td style="width: 43%;">
<div>The calculated MD5 hash for the creative.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>creative_is_video</strong></div>
</td>
<td style="width: 43%;">
<div>True if the creative is a video, false otherwise.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>creative_url</strong></div>
</td>
<td style="width: 43%;">
<div>The URL of the creative (or ad).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>creative_image_hash</strong></div>
</td>
<td style="width: 43%;">
<div>The calculated MD5 hash specifically for the image (in contrast with <strong>creative_hash</strong>, which is a hash for the entire contents of any creative, including text).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>data_connector_id</strong></div>
</td>
<td style="width: 43%;">
<div>The ID of the data connector through which the data was pulled.<br><br><strong>Note on "data connector" vs. "source":</strong> In Singular, a <strong>"source"</strong> is an ad network partner from which Singular pulls your advertising data. A <strong>"data connector"</strong> is a tool that connects to an ad network and pulls data. You may have multiple data connectors sharing the same source. This means they pull data into Singular from the same platform (but with different account names, settings, etc.).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>data_connector_source_name</strong></div>
</td>
<td style="width: 43%;">
<div>The ad network that the data connector pulled data from.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>data_connector_timestamp_utc</strong></div>
</td>
<td style="width: 43%;">
<div>The date and time in which Singular started pulling data from the network. This tells you how fresh the data is.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>data_connector_username</strong></div>
</td>
<td style="width: 43%;">
<div>&nbsp;</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>singular_campaign_id</strong></div>
</td>
<td style="width: 43%;">
<div>The campaign ID in Singular. This may be different from the original campaign ID - for example, if there are duplicates.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em>N/A *</em></div>
</td>
<td style="width: 15%;">
<div><strong>singular_creative_id</strong></div>
</td>
<td style="width: 43%;">
<div>An identifier given by Singular to the creative. This may be different from the original ID pulled from the ad network or the tracker (for example, if there are duplicates).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="always-visible">
<td style="background-color: #3089f4; width: 15%;">
<h2 style="color: #ffffff; font-size: large; font-weight: bold; margin: 0;">Metrics</h2>
</td>
<td style="background-color: #3089f4; width: 15%;"><span style="color: #ffffff; font-size: large;"><strong>&nbsp;</strong></span></td>
<td style="background-color: #3089f4; width: 43%;"><span style="color: #ffffff; font-size: large;"><strong>&nbsp;</strong></span></td>
<td style="background-color: #3089f4; width: 15%;"><span style="color: #ffffff; font-size: large;"><strong>&nbsp;</strong></span></td>
<td style="background-color: #3089f4; width: 12%;"><span style="color: #ffffff; font-size: large;"><strong>&nbsp;</strong></span></td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad ARPDAU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Average revenue from ad monetization per daily active user.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad ARPU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Average revenue from ad monetization per user.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Clicks</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_clicks</strong></div>
</td>
<td style="width: 43%;">
<div>The number of times a user clicked on an ad.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Impressions</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_impressions</strong></div>
</td>
<td style="width: 43%;">
<div>How many times ads were viewed in your app (as reported by the network). This includes both videos and static ads.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Requests</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_requests</strong></div>
</td>
<td style="width: 43%;">
<div>How many times your app contacted the network requesting an ad to display.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Ad Revenue</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_revenue</strong></div>
</td>
<td style="width: 43%;">
<div>The aggregated revenue reported by the network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>ARPDAU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Average revenue per daily active user.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>ARPU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Average revenue per user.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Average Frequency<br></strong></div>
</td>
<td style="width: 15%;"><strong>frequency</strong><em><br></em></td>
<td style="width: 43%;">
<div>The average number of times each person saw your ad.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Bid Requests</strong></div>
</td>
<td style="width: 15%;">
<div><strong>bid_requests</strong></div>
</td>
<td style="width: 43%;">
<div>The number of requests by the publisher to open an auction. Currently only applicable to Facebook’s RTB.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Bid Responses</strong></div>
</td>
<td style="width: 15%;">
<div><strong>bid_responses</strong></div>
</td>
<td style="width: 43%;">
<div>The number of bids responded to by the auction, i.e. the bid payload for each bid. Currently only applicable to Facebook’s RTB.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Clicks</strong></div>
</td>
<td style="width: 15%;">
<div><strong>custom_clicks</strong></div>
</td>
<td style="width: 43%;">
<div>Number of ad clicks. By default, this metric is pulled from the tracker side, but it can be set up to show clicks reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Clicks</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_report_network_clicks</strong></div>
</td>
<td style="width: 43%;">
<div>Clicks as reported by the ad network</div>
</td>
<td style="width: 15%;">
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Clicks Discrepancy</strong></div>
</td>
<td style="width: 15%;">
<div><strong>clicks_discrepancy</strong></div>
</td>
<td style="width: 43%;">
<div>The difference between clicks reported by the tracker and clicks reported by the network. Use this metric to help you identify and troubleshoot major discrepancies. Formula: Tracker Clicks - Network Clicks</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Comments<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_comments</strong><em><br></em></div>
</td>
<td style="width: 43%;">
<div>Number of ad comments as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Completed Video View Rate</strong></div>
</td>
<td style="width: 15%;">
<div><em>N/A #</em></div>
</td>
<td style="width: 43%;">
<div>Percentage of videos that were viewed in their entirety out of videos that were initiated. Formula: (Completed Video Views / Video Views) * 100</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Completed Video Views</strong></div>
</td>
<td style="width: 15%;">
<div><strong>completed_video_views</strong></div>
</td>
<td style="width: 43%;">
<div>How many videos were viewed in their entirety.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Completed Video Views</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_completed_video_views</strong></div>
</td>
<td style="width: 43%;">
<div>How many users viewed a video in its entirety. Note that not all networks provide this information.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Completed Video View Rate</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Percentage of videos that were viewed in their entirety out of videos that were initiated. Formula: (Completed Video Views / Video Views) * 100</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Conversion Values - Count</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_conversion_values_count</strong></div>
</td>
<td style="width: 43%;">The number of SKAN installs for which Singular has received a conversion value (including conversion value 0 but not including conversion value Null).</td>
<td style="width: 15%;">
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;"><strong>Conversion Values - Ratio</strong></td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">The percentage of SKAN installs for which Singular has received a conversion value (including conversion value 0 but not including conversion value Null). This is equal to <strong>Conversion Values Count / SKAN Installs</strong>.</td>
<td style="width: 15%;">
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Cost</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_cost</strong></div>
</td>
<td style="width: 43%;">
<div>Cost (ad spend) reported by the ad network, in your default currency configured in Singular.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>CTR</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Click-through rate (ratio of clicks to impressions).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>CVR</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Conversion rate (ratio of installs to clicks).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>DAU</strong></div>
</td>
<td style="width: 15%;">
<div><strong>daily_active_users</strong></div>
</td>
<td style="width: 43%;">
<div>Daily Active Users: Number of unique users who had at least one session in the day. The day is the rolling day since the user's time of attribution. For periods of more than one day, the DAU is the average of the daily active users for the selected days.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>eCPC</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective Cost per Click: the total cost divided by the total click count.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>eCPCV</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective cost per completed view. Formula: Revenue / Completed Video Views</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>eCPI</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective Cost per Install: the total cost divided by the total install count.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>eCPI (Orig. Cost)</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective Cost per Install, but based on the original cost, before any currency conversions.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>eCPM</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective Cost per Mille: the cost per 1000 impressions.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>eCPM</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective cost per one thousand impressions.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>eCPV</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective cost per view. Formula: Revenue / Video Views</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Est. Conversions</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_estimated_total_conversions</strong></div>
</td>
<td style="width: 43%;">
<div>An estimate of total conversions as reported by the ad network (when available).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em><strong>Estimated Revenue</strong></em></div>
</td>
<td style="width: 15%;">
<div><em><strong>skan_estimated_revenue</strong></em></div>
</td>
<td style="width: 43%;">
<div><em>Revenue from campaigns that use a Revenue-type model. <strong>Update (April 2022): This metric will be deprecated. Use SKAN Revenue instead.</strong></em></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><em><strong>Estimated ROI</strong></em></div>
</td>
<td style="width: 15%;">
<div><em><strong>skan_estimated_ROI</strong></em></div>
</td>
<td style="width: 43%;">
<div><em>ROI calculated based on skan_estimated_revenue. <strong>Update (April 2022): This metric will be deprecated. Use SKAN ROI instead.</strong><br></em></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Filled Ad Requests</strong></div>
</td>
<td style="width: 15%;">
<div><strong>filled_ad_requests</strong></div>
</td>
<td style="width: 43%;">
<div>How many ads the network served after receiving a request.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Fill Rate</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Percentage of ad requests that were answered by the network. Formula: (Filled Ad Requests / Ad Requests) * 100</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Impressions</strong></div>
</td>
<td style="width: 15%;">
<div><strong>custom_impressions</strong></div>
</td>
<td style="width: 43%;">
<div>Number of ad views. By default, this metric is pulled from the network side.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Impressions</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_report_network_impressions</strong></div>
</td>
<td style="width: 43%;">
<div>Number of ad views as measured by the ad network.</div>
</td>
<td style="width: 15%;">
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Impressions Discrepancy</strong></div>
</td>
<td style="width: 15%;">
<div><strong>impressions_discrepancy</strong></div>
</td>
<td style="width: 43%;">
<div>The difference between impressions reported by the tracker and impressions reported by the network. Use this metric to identify and troubleshoot major discrepancies. Formula: Tracker Impressions - Network Impressions</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Installs</strong></div>
</td>
<td style="width: 15%;">
<div><strong>custom_installs</strong></div>
</td>
<td style="width: 43%;">
<div>Installs as displayed in the Singular UI. This is a custom field and can be set to show network-side installs for some sources and tracker-side installs for other sources.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Installs Discrepancy</strong></div>
</td>
<td style="width: 15%;">
<div><strong>installs_discrepancy</strong></div>
</td>
<td style="width: 43%;">
<div>The difference between installs reported by the tracker and installs reported by the network. Use this metric to help you identify and troubleshoot major discrepancies. Formula: Tracker Installs - Network Installs</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Likes<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_likes<br></strong></div>
</td>
<td style="width: 43%;">
<div>Number of ad likes as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Clicks</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_clicks</strong></div>
</td>
<td style="width: 43%;">
<div>The number of ad clicks as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Impressions</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_impressions</strong></div>
</td>
<td style="width: 43%;">
<div>The number of ad views as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Network Installs</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_installs</strong></div>
</td>
<td style="width: 43%;">
<div>The number of app installs as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>New Visitors</strong></div>
</td>
<td style="width: 15%;">
<div><strong>new_visitors</strong></div>
</td>
<td style="width: 43%;">
<div><span>The number of users who've visited your site for the first time.</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>oCVR</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Conversion rate from impressions to installs (the number of installs divided by impressions).</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Cost</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_original_cost</strong></div>
</td>
<td style="width: 43%;">
<div>Original cost (presented in the original currency) reported by the ad network. In API queries, we recommend using this metric only when using the "adn_original_currency" dimension</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Currency</strong></div>
</td>
<td style="width: 15%;">
<div><strong>adn_original_currency</strong></div>
</td>
<td style="width: 43%;">
<div>The currency of the Original Cost value.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Original Revenue</strong></div>
</td>
<td style="width: 15%;">
<div><strong>original_revenue</strong></div>
</td>
<td style="width: 43%;">
<div>If there are any custom calculations applied to the "Revenue" metric in your account, use "Original Revenue" to see the original revenue value as reported by the source.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Page Follows<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>page_follows</strong><strong><br></strong></div>
</td>
<td style="width: 43%;">
<div>Number of new followers generated from ads as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Posts saved</strong></div>
</td>
<td style="width: 15%;">
<div><strong>posts_saved</strong><em><br></em></div>
</td>
<td style="width: 43%;">
<div>Number of post saves as reported by the ad network.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Re-engaged Visitors</strong></div>
</td>
<td style="width: 15%;">
<div><strong>re_engaged_visitors</strong></div>
</td>
<td style="width: 43%;">
<div><span>The number of users who've been brought back to your site by a re-engagement campaign.</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Re-Engagements</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_reengagements</strong></div>
</td>
<td style="width: 43%;">
<div>Number of re-engaged users.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Reach<br></strong></div>
</td>
<td style="width: 15%;">
<div><strong>reach</strong><strong><br></strong></div>
</td>
<td style="width: 43%;">
<div>The number of people who saw your ads at least once.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Retained Users<br></strong></div>
</td>
<td style="width: 15%;">
<div><em>N/A**</em><strong><br></strong></div>
</td>
<td style="width: 43%;">
<div>The number of users still active in the app (sending sessions to Singular) after the number of days specified in the cohort period(s). E.g., "Retained Users 7d" - the number of users still active 7 days after the install.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Retention Rate<br></strong></div>
</td>
<td style="width: 15%;">
<div><em>N/A #</em></div>
</td>
<td style="width: 43%;">
<div>The percentage of users still active in the app (sending sessions to Singular) after the number of days specified in the cohort period(s). E.g., "Retention Rate 7d" - the percentage of users still active 7 days after the install. Equal to the Retained Users for that cohort period divided by the installs.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Revenue</strong></div>
</td>
<td style="width: 15%;">
<div><strong>revenue</strong></div>
</td>
<td style="width: 43%;">
<div>The revenue gained from the cohort of users in the selected cohort period.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>ROI</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Return on Investment (return on ad spend): the revenue divided by the cost.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Shares<br></strong></div>
</td>
<td style="width: 15%;"><strong>adn_shares</strong><em><br></em></td>
<td style="width: 43%;"><span>Number of ad shares as reported by the ad network.<br></span></td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Show Rate</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;"><span>Percentage of ads viewed out of all filled ad requests. Formula: (Impressions / Filled Ad Requests) * 100</span></td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN eCPI</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Effective Cost per Install: the total cost divided by the number of SKAN installs.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN Installs</strong></div>
</td>
<td style="width: 15%;">
<div><strong>skan_installs</strong></div>
</td>
<td style="width: 43%;">
<div>Number of installs as reported by SKAdNetwork.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-raw" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Raw_Data_FAQ">SKAN Raw</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN oCVR</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Conversion rate from impressions to SKAN installs.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN Revenue<br></strong></div>
</td>
<td style="width: 15%;"><strong>skan_revenue</strong></td>
<td style="width: 43%;">
<div>Any revenue gained from campaigns, regardless of the conversion model used.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>SKAN ROI<br></strong></div>
</td>
<td style="width: 15%;"><strong>skan_roi</strong></td>
<td style="width: 43%;">
<div>ROI calculated based on skan_revenue.</div>
</td>
<td style="width: 15%;">
<div class="tag-list">
<ul>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Total ARPDAU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>The total revenue divided by the number of daily active users.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Total ARPU</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>The total revenue divided by the number of users.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Total Revenue</strong></div>
</td>
<td style="width: 15%;">
<div><strong>total_revenue</strong></div>
</td>
<td style="width: 43%;">
<div>The total revenue gained from ad monetization as well as in-app purchases&nbsp;from the cohort of users in the selected cohort period.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Total ROI</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div>Return on Investment: The total revenue divided by the cost.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Total Web Conversions</strong></div>
</td>
<td style="width: 15%;"><strong>total_web_conversions</strong></td>
<td style="width: 43%;">
<div><span>Sum of new visitors and re-engaged visitors.</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-web" href="https://support.singular.net/hc/en-us/articles/5443693313179">Web</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Clicks</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_clicks</strong></div>
</td>
<td style="width: 43%;">
<div>Clicks reported by the attribution tracker.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 15%;">
<div><strong>Tracker Installs</strong></div>
</td>
<td style="width: 15%;">
<div><strong>tracker_installs</strong></div>
</td>
<td style="width: 43%;">
<div>Number of installs as reported by the attribution tracker.<br><br>For <strong>SKAdNetwork Reports</strong>, these are installs that were attributed by the tracker based on device matching, as opposed to "SKAN Installs", which are based on SKAdNetwork postbacks. See <a href="https://support.singular.net/hc/en-us/articles/360054483191--New-SKAdNetwork-Reporting-FAQ#tracker_installs" target="_self">What are tracker installs?</a></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-general" href="https://support.singular.net/hc/en-us/articles/205046069-Reports-FAQ">General</a></li>
<li><a class="tag-skadnetwork-report" href="https://support.singular.net/hc/en-us/articles/360054483191#SKAdNetwork_Reports_FAQ">SKAN Report</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Video Views</strong></div>
</td>
<td style="width: 15%;">
<div><strong>video_views</strong></div>
</td>
<td style="width: 43%;">
<div>How many videos were initiated. Depending on the network and ad type, this metric may be the same as "ad impressions".</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Video Views</strong></div>
</td>
<td style="width: 15%;">
<div><strong>ad_video_views</strong></div>
</td>
<td style="width: 43%;">
<div>How many videos were initiated. This metric can sometimes be the same as ad impressions. It depends on the network and the ad type.</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Video Views 25%</strong></div>
</td>
<td style="width: 15%;">
<div><strong>video_views_25pct</strong></div>
</td>
<td style="width: 43%;">
<div>The number of impressions where the viewer watched the video to the 25% point. Formula: impressions x video view rate</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Video Views 50%</strong></div>
</td>
<td style="width: 15%;">
<div><strong>video_views_50pct</strong></div>
</td>
<td style="width: 43%;">
<div>The number of impressions where the viewer watched the video to the halfway point. Formula: impressions x video view rate</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Video Views 75%</strong></div>
</td>
<td style="width: 15%;">
<div><strong>video_views_75pct</strong></div>
</td>
<td style="width: 43%;">
<div>The number of impressions where the viewer watched the video to the 75% point. Formula: impressions x video view rate</div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-creatives" href="https://support.singular.net/hc/en-us/articles/115001862443">Creatives</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">
<div>&nbsp;</div>
</td>
</tr>
<tr class="hidden-row">
<td style="width: 15%;">
<div><strong>Win Rate</strong></div>
</td>
<td style="width: 15%;"><em>N/A #</em></td>
<td style="width: 43%;">
<div><span>Percentage of bid responses against the number of requests. Formula: (100 * bid responses / bid requests)</span></div>
</td>
<td style="width: 15%;">
<div>
<ul class="tag-list">
<li><a class="tag-ad-mon" href="https://support.singular.net/hc/en-us/articles/360022067552-Ad-Monetization-Analytics-FAQ">Ad Mon</a></li>
</ul>
</div>
</td>
<td style="width: 12%;">&nbsp;</td>
</tr>
</tbody>
</table>

"""


if __name__ == '__main__':
    main(write_table=False)

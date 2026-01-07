# src/tools/ads.py
from typing import Dict, List, Optional
from src.app import mcp
from src.config import FB_GRAPH_URL
from src.helpers import _get_fb_access_token, _make_graph_api_call, _prepare_params

@mcp.tool()
def get_ad_by_id(ad_id: str, fields: Optional[List[str]] = None) -> Dict:
    """Retrieves detailed information about a specific Facebook ad by its ID."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}"
    params = _prepare_params({'access_token': access_token}, fields=fields)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_ads_by_adaccount(act_id: str, **kwargs) -> Dict:
    """Retrieves ads from a specific Facebook ad account."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/ads"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_ads_by_campaign(campaign_id: str, **kwargs) -> Dict:
    """Retrieves ads associated with a specific Facebook campaign."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/ads"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_ads_by_adset(adset_id: str, **kwargs) -> Dict:
    """Retrieves ads associated with a specific Facebook ad set."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/ads"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

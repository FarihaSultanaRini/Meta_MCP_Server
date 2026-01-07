# src/tools/adsets.py
from typing import Dict, List, Optional
from src.app import mcp
from src.config import FB_GRAPH_URL
from src.helpers import _get_fb_access_token, _make_graph_api_call, _prepare_params

@mcp.tool()
def get_adset_by_id(adset_id: str, fields: Optional[List[str]] = None) -> Dict:
    """Retrieves detailed information about a specific Facebook ad set by its ID."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}"
    params = _prepare_params({'access_token': access_token}, fields=fields)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_adsets_by_ids(adset_ids: List[str], **kwargs) -> Dict:
    """Retrieves detailed information about multiple Facebook ad sets by their IDs."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/"
    params = _prepare_params({
        'access_token': access_token,
        'ids': ','.join(adset_ids)
    }, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_adsets_by_adaccount(act_id: str, **kwargs) -> Dict:
    """Retrieves ad sets from a specific Facebook ad account."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/adsets"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_adsets_by_campaign(campaign_id: str, **kwargs) -> Dict:
    """Retrieves ad sets associated with a specific Facebook campaign."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/adsets"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

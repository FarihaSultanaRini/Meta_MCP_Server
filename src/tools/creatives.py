# src/tools/creatives.py
from typing import Dict, List, Optional
from src.app import mcp
from src.config import FB_GRAPH_URL
from src.helpers import _get_fb_access_token, _make_graph_api_call, _prepare_params

@mcp.tool()
def get_ad_creative_by_id(creative_id: str, **kwargs) -> Dict:
    """Retrieves detailed information about a specific Facebook ad creative."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{creative_id}"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_ad_creatives_by_ad_id(ad_id: str, **kwargs) -> Dict:
    """Retrieves the ad creatives associated with a specific Facebook ad."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}/adcreatives"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

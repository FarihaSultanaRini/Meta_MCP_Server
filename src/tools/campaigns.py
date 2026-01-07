# src/tools/campaigns.py
from typing import Dict, List, Optional
from src.app import mcp
from src.config import FB_GRAPH_URL
from src.helpers import _get_fb_access_token, _make_graph_api_call, _prepare_params

@mcp.tool()
def get_campaign_by_id(campaign_id: str, **kwargs) -> Dict:
    """Retrieves detailed information about a specific Facebook ad campaign by its ID."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_campaigns_by_adaccount(act_id: str, **kwargs) -> Dict:
    """Retrieves campaigns from a specific Facebook ad account."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/campaigns"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

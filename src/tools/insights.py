# src/tools/insights.py
import requests
from typing import Dict, List, Optional, Any
from src.app import mcp
from src.config import FB_GRAPH_URL
from src.helpers import _get_fb_access_token, _make_graph_api_call, _build_insights_params

@mcp.tool()
def get_adaccount_insights(act_id: str, **kwargs) -> Dict:
    """Retrieves performance insights for a specified Facebook ad account."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/insights"
    params = _build_insights_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_campaign_insights(campaign_id: str, **kwargs) -> Dict:
    """Retrieves performance insights for a specific Facebook ad campaign."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/insights"
    effective_level = kwargs.get('level', 'campaign')
    params = _build_insights_params({'access_token': access_token}, level=effective_level, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_adset_insights(adset_id: str, **kwargs) -> Dict:
    """Retrieves performance insights for a specific Facebook ad set."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/insights"
    effective_level = kwargs.get('level', 'adset')
    params = _build_insights_params({'access_token': access_token}, level=effective_level, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_ad_insights(ad_id: str, **kwargs) -> Dict:
    """Retrieves detailed performance insights for a specific Facebook ad."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}/insights"
    effective_level = kwargs.get('level', 'ad')
    params = _build_insights_params({'access_token': access_token}, level=effective_level, **kwargs)
    return _make_graph_api_call(url, params)

@mcp.tool()
def fetch_pagination_url(url: str) -> Dict:
    """Fetch data from a Facebook Graph API pagination URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# src/tools/activities.py
from typing import Dict
from src.app import mcp
from src.helpers import _fetch_edge

@mcp.tool()
def get_activities_by_adaccount(act_id: str, **kwargs) -> Dict:
    """Retrieves activities for a Facebook ad account."""
    return _fetch_edge(parent_id=act_id, edge_name='activities', **kwargs)

@mcp.tool()
def get_activities_by_adset(adset_id: str, **kwargs) -> Dict:
    """Retrieves activities for a Facebook ad set."""
    return _fetch_edge(parent_id=adset_id, edge_name='activities', **kwargs)

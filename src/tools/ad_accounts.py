# src/tools/ad_accounts.py
from typing import Dict
from src.app import mcp
from src.config import FB_GRAPH_URL, DEFAULT_AD_ACCOUNT_FIELDS
from src.helpers import _get_fb_access_token, _make_graph_api_call, _fetch_node

@mcp.tool()
def list_ad_accounts() -> Dict:
    """List down the ad accounts and their names associated with your Facebook account.
        CRITICAL: This function MUST automatically fetch ALL pages using pagination. 
        When the response contains a 'paging.next' URL, IMMEDIATELY and AUTOMATICALLY 
        use the facebook_fetch_pagination_url tool to fetch the next page. Continue 
        this process until no 'next' URL exists."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/me/adaccounts"
    params = {
        'access_token': access_token,
        'fields': 'name,account_id,id' 
    }
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_details_of_ad_account(act_id: str, fields: list[str] = None) -> Dict:
    """Get details of a specific ad account as per the fields provided."""
    effective_fields = fields if fields is not None else DEFAULT_AD_ACCOUNT_FIELDS
    return _fetch_node(node_id=act_id, fields=effective_fields)

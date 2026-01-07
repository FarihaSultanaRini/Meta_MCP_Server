# src/main.py
import os
import sys

# Ensure the src directory is in the path if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import mcp
from src.config import FB_GRAPH_URL, DEFAULT_AD_ACCOUNT_FIELDS
from src.helpers import _get_fb_access_token, _make_graph_api_call, _fetch_node

# Import tools to register them with the FastMCP instance
from src.tools import (
    ad_accounts,
    insights,
    ads,
    adsets,
    campaigns,
    creatives,
    activities
)

if __name__ == "__main__":
    # Ensure token is valid/configured before running
    try:
        _get_fb_access_token()
    except Exception as e:
        sys.stderr.write(f"Configuration Error: {e}\n")
        # Don't exit here, mcp.run might handle it or wait for dynamic config if implemented later
    
    # Run the server
    mcp.run(transport='stdio')

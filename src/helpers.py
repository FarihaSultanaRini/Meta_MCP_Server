# src/helpers.py
import sys
import os
import json
import requests
from typing import Dict, Any, List, Optional
from .config import FB_GRAPH_URL

# Global variable for token caching
FB_ACCESS_TOKEN = None

def _get_fb_access_token() -> str:
    """Gets the FB access token from args, env, or .env file."""
    global FB_ACCESS_TOKEN
    if FB_ACCESS_TOKEN is not None:
        return FB_ACCESS_TOKEN

    # 1. Command line argument
    if "--fb-token" in sys.argv:
        try:
            token_index = sys.argv.index("--fb-token") + 1
            if token_index < len(sys.argv):
                FB_ACCESS_TOKEN = sys.argv[token_index]
                return FB_ACCESS_TOKEN
        except ValueError:
            pass

    # 2. Environment variable
    FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
    if FB_ACCESS_TOKEN:
        return FB_ACCESS_TOKEN

    # 3. .env file manual check (fallback)
    try:
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("FB_ACCESS_TOKEN="):
                        FB_ACCESS_TOKEN = line.split("=", 1)[1].strip()
                        return FB_ACCESS_TOKEN
    except Exception:
        pass

    if FB_ACCESS_TOKEN is None:
        raise Exception("Facebook token must be provided via '--fb-token' argument or 'FB_ACCESS_TOKEN' environment variable")
    
    return FB_ACCESS_TOKEN

def _make_graph_api_call(url: str, params: Dict[str, Any]) -> Dict:
    """Makes a GET request to the FB Graph API and handles detailed error reporting."""
    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            try:
                error_data = response.json().get('error', {})
                error_message = error_data.get('message', 'Unknown error')
                error_type = error_data.get('type', 'UnknownType')
                error_code = error_data.get('code', 'UnknownCode')
                error_subcode = error_data.get('error_subcode', '')
                
                full_error_msg = f"Facebook API Error ({response.status_code}): {error_message} (Type: {error_type}, Code: {error_code}"
                if error_subcode:
                    full_error_msg += f", Subcode: {error_subcode}"
                full_error_msg += ")"
                
                sys.stderr.write(f"{full_error_msg}\n")
                raise Exception(full_error_msg)
            except (ValueError, KeyError, AttributeError):
                sys.stderr.write(f"FB API Error Body: {response.text}\n")
                response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Error making Graph API call to {url}: {e}\n")
        raise

def _prepare_params(base_params: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Prepares and JSON-encodes parameters for Graph API calls."""
    params = base_params.copy()
    json_fields = [
        'filtering', 'time_range', 'time_ranges', 'effective_status', 
        'special_ad_categories', 'objective', 'buyer_guarantee_agreement_status'
    ]
    comma_fields = ['fields', 'action_attribution_windows', 'action_breakdowns', 'breakdowns']

    for key, value in kwargs.items():
        if value is not None:
            if key in json_fields and isinstance(value, (list, dict)):
                params[key] = json.dumps(value)
            elif key in comma_fields and isinstance(value, list):
                params[key] = ','.join(value)
            else:
                params[key] = value
    return params

def _fetch_node(node_id: str, **kwargs) -> Dict:
    """Helper to fetch a single object (node) by its ID."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{node_id}"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

def _fetch_edge(parent_id: str, edge_name: str, **kwargs) -> Dict:
    """Helper to fetch a collection (edge) related to a parent object."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{parent_id}/{edge_name}"
    
    # Special timeline params for 'activities' edge
    time_params = {}
    if edge_name == 'activities':
        for key in ['time_range', 'since', 'until']:
            if key in kwargs:
                time_params[key] = kwargs.pop(key)
            
    base_params = {'access_token': access_token}
    params = _prepare_params(base_params, **kwargs)
    if time_params:
        params.update(_prepare_params({}, **time_params))

    return _make_graph_api_call(url, params)

def _build_insights_params(params: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Builds complex parameter set for insights API calls."""
    # Use generic builder first
    params = _prepare_params(params, **kwargs)

    # Specific logic for date/time presets vs ranges
    time_range = kwargs.get('time_range')
    time_ranges = kwargs.get('time_ranges')
    since = kwargs.get('since')
    until = kwargs.get('until')
    date_preset = kwargs.get('date_preset')
    time_increment = kwargs.get('time_increment')

    if not (time_range or time_ranges or since or until) and date_preset:
        params['date_preset'] = date_preset
    
    if time_range: params['time_range'] = json.dumps(time_range)
    if time_ranges: params['time_ranges'] = json.dumps(time_ranges)
    if time_increment and time_increment != 'all_days':
        params['time_increment'] = time_increment
        
    if not (time_range or time_ranges):
        if since: params['since'] = since
        if until: params['until'] = until

    # Boolean flags as strings
    for flag in ['default_summary', 'use_account_attribution_setting', 'use_unified_attribution_setting']:
        if kwargs.get(flag):
            params[flag] = 'true'

    return params

# Challenge: Script to pull top alerts from Prometheus API.
# Focus: APIs, metrics
# Example Hint: Use requests, Prometheus queries

import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

# Prometheus API configuration
PROMETHEUS_URL = "http://127.0.0.1:9090"  # Replace with your Prometheus server URL
ALERTS_ENDPOINT = "/api/v1/alerts"
QUERY_ENDPOINT = "/api/v1/query"

# Authentication (if needed)
USERNAME = None  # Set if authentication is required
PASSWORD = None  # Set if authentication is required

def get_active_alerts():
    """Fetch all active alerts from Prometheus"""
    url = f"{PROMETHEUS_URL}{ALERTS_ENDPOINT}"
    
    try:
        if USERNAME and PASSWORD:
            response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        data = response.json()
        
        # Filter for active alerts (state='firing')
        active_alerts = [alert for alert in data['data']['alerts'] 
                        if alert['state'].lower() == 'firing']
        
        return active_alerts
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching alerts: {e}")
        return None

def get_top_alerts_by_metric(metric_name, limit=5):
    """Get top alerts by a specific metric value"""
    query = f'topk({limit}, {metric_name})'
    url = f"{PROMETHEUS_URL}{QUERY_ENDPOINT}?query={query}"
    
    try:
        if USERNAME and PASSWORD:
            response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        data = response.json()
        
        return data['data']['result']
        
    except requests.exceptions.RequestException as e:
        print(f"Error querying metric: {e}")
        return None

def display_alerts(alerts):
    """Display alerts in a readable format"""
    if not alerts:
        print("No active alerts found.")
        return
    
    print(f"\n=== Active Alerts ({len(alerts)}) ===\n")
    for i, alert in enumerate(alerts, 1):
        print(f"Alert #{i}:")
        print(f"  Name:        {alert['labels'].get('alertname', 'N/A')}")
        print(f"  Severity:    {alert['labels'].get('severity', 'N/A')}")
        print(f"  State:       {alert['state']}")
        print(f"  Summary:     {alert['annotations'].get('summary', 'N/A')}")
        print(f"  Description: {alert['annotations'].get('description', 'N/A')}")
        
        # Convert timestamp to readable format
        if 'activeAt' in alert:
            active_at = datetime.strptime(alert['activeAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"  Active Since: {active_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "-"*50 + "\n")

def main():
    print("Fetching active alerts from Prometheus...")
    
    # Option 1: Get all active alerts
    active_alerts = get_active_alerts()
    display_alerts(active_alerts)
    
    # Option 2: Get top alerts by a specific metric (example with CPU usage)
    # metric_name = "node_cpu_seconds_total"
    # top_alerts = get_top_alerts_by_metric(metric_name)
    # print(f"Top alerts by {metric_name}:")
    # print(json.dumps(top_alerts, indent=2))

if __name__ == "__main__":
    main()

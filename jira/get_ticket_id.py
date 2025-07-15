import json
import requests
from requests.auth import HTTPBasicAuth
import sys

def load_jira_config():
    """Load Jira configuration from JSON file"""
    with open('data/jira_config.json') as f:
        return json.load(f)

def get_ticket_id(ticket_key):
    """Get Jira ticket ID by ticket key"""
    config = load_jira_config()
    
    # Set up API endpoint and auth
    url = f"{config['JiraUrl']}/rest/api/3/issue/{ticket_key}"
    auth = HTTPBasicAuth(config['user'], config['JiraToken'])
    
    # Make API request
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('id')
    else:
        print(f"Error fetching ticket: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticket_key = sys.argv[1]
        ticket_id = get_ticket_id(ticket_key)
        if ticket_id:
            print(f"Ticket ID for {ticket_key}: {ticket_id}")
        else:
            print(f"Failed to get ID for ticket {ticket_key}")
    else:
        print("Usage: python get_ticket_id.py <ticket_key>")

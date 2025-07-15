import json
import requests
from requests.auth import HTTPBasicAuth
import sys

def load_jira_config():
    """Load Jira configuration from JSON file"""
    with open('data/jira_config.json') as f:
        return json.load(f)

def get_ticket_details(ticket_key):
    """Get detailed information about a Jira ticket"""
    config = load_jira_config()
    
    # Set up API endpoint and auth
    url = f"{config['JiraUrl']}/rest/api/3/issue/{ticket_key}"
    auth = HTTPBasicAuth(config['user'], config['JiraToken'])
    
    # Fields to fetch from Jira
    fields = [
        'summary',  # Title
        'description',
        'customfield_10026',  # Acceptance Criteria (common field ID)
        'status',
        'priority',
        'assignee'
    ]
    
    # Make API request
    headers = {"Accept": "application/json"}
    params = {'fields': ','.join(fields)}
    response = requests.get(url, headers=headers, auth=auth, params=params)
    
    if response.status_code == 200:
        data = response.json()
        fields = data.get('fields', {})
        
        # Format the output
        details = {
            'Title': fields.get('summary'),
            'Description': fields.get('description'),
            'Acceptance Criteria': fields.get('customfield_10026'),
            'Status': fields.get('status', {}).get('name') if fields.get('status') else None,
            'Priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
            'Assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None
        }
        return details
    else:
        print(f"Error fetching ticket details: {response.status_code} - {response.text}")
        return None

def print_ticket_details(details):
    """Print ticket details in a readable format"""
    if not details:
        return
        
    print("\nJira Ticket Details:")
    print("-------------------")
    for key, value in details.items():
        print(f"{key}: {value if value else 'Not available'}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticket_key = sys.argv[1]
        details = get_ticket_details(ticket_key)
        if details:
            print_ticket_details(details)
        else:
            print(f"Failed to get details for ticket {ticket_key}")
    else:
        print("Usage: python get_ticket_details.py <ticket_key>")

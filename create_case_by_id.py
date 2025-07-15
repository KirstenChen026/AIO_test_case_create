import sys
import os
from pathlib import Path
import json
import requests
from typing import Optional, List
from util.get_config import Jira_Config

def create_aio_test_case_with_jira_link(
    project: str,    
    name: str,
    description: str,
    precondition: str,
    test_steps: List[dict],
    jira_requirement_ids: List[str],
    folder_id: Optional[str] = None
) -> Optional[dict]:
    """
    Creates an AIO Test Case and links it to specified Jira Requirement IDs.
    Modified version that accepts external requirement IDs.
    """
    jira_config = Jira_Config()

    project_key = project
    aio_base_url = jira_config.get_aio_url() + f"/project/{project_key}"
    api_token = jira_config.get_aio_token()

    if not api_token:
        print("Error: API_TOKEN not set.")
        return None

    headers = {
        "accept": "application/json;charset=utf-8",
        "Authorization": f"AioAuth {api_token}"
    }

    test_case_data = {
        "title": name,
        "description": description,
        "precondition": precondition,
        "steps": test_steps,
        "status": {"name": "Under Review"},
        "jiraRequirementIDs": jira_requirement_ids,
        "scriptType": {"name": "Classic"}
    }

    if folder_id:
        test_case_data["folderID"] = folder_id

    create_tc_url = f"{aio_base_url}/testcase"

    print(f"Creating test case: '{name}'")
    print(f"Linking to Jira IDs: {jira_requirement_ids}")
    print(f"Request URL: {create_tc_url}")
    print(f"Request Payload: {json.dumps(test_case_data, indent=2)}")

    try:
        response = requests.post(create_tc_url, headers=headers, json=test_case_data)
        response.raise_for_status()
        print("\nTest Case created successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating test case: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
    return None

def get_jira_ids_from_file(file_path: str) -> List[str]:
    """Read Jira ticket keys from JSON file and convert to IDs"""
    try:
        with open(file_path) as f:
            data = json.load(f)
            keys = data.get('jira_ticket_keys', [])
            project = data.get('project', 'RAA')
            
            # If keys are in format KEY-123, we'll need to convert them to IDs
            # For now return as-is - can add conversion logic later if needed
            return keys
            
    except Exception as e:
        print(f"Error reading Jira requirements file: {e}")
        return []

if __name__ == "__main__":
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create AIO test case linked to Jira requirements')
    parser.add_argument('--project', required=True, help='Jira project key')
    parser.add_argument('--name', required=True, help='Test case name')
    parser.add_argument('--description', default='', help='Test case description')
    parser.add_argument('--precondition', default='', help='Test case preconditions')
    parser.add_argument('--steps', required=True, help='JSON array of test steps')
    parser.add_argument('--jira_ids', required=True, help='JSON array of Jira requirement IDs')
    
    args = parser.parse_args()
    
    try:
        steps = json.loads(args.steps)
        jira_ids = json.loads(args.jira_ids)
        
        result = create_aio_test_case_with_jira_link(
            project=args.project,
            name=args.name,
            description=args.description,
            precondition=args.precondition,
            test_steps=steps,
            jira_requirement_ids=jira_ids
        )
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}")
        sys.exit(1)

    if result:
        print("\nCreated Test Case Details:")
        print(json.dumps(result, indent=2))

# Jira to AIO Test Case Workflow

## Purpose
This workflow demonstrates how to:
1. Extract Jira ticket details
2. Create test case documentation 
3. Generate AIO test cases through API
4. Link to original Jira ticket

## Prerequisites
<!-- - Connected MCP server with Jira integration   -->
- Valid Jira and AIO API credentials 
- Test case descriptions from Jira tickets

## Workflow Steps

1. **Get Jira Ticket**
   - Input: Jira key (e.g. "PROJ-123")
   - Actions:
     - Get Jira Porject Key from Jira key(e.g. "PROJ")
     - Query ticket details using `Jira/get_ticket_details.py`
     - Extract title, description and acceptance criteria
     - Get internal ticket ID using `Jira/get_ticket_id.py`

2. **Create Test Case Documentation**
   - use template Jira/AIO/test_cases/TEST_CASE_TEMPLATE.md
   - Output:
     - Markdown file with:
       - Jira internal ticket ID
       - Test case title (from Jira name)
       - Test case name
       - Preconditions  
       - Test steps (from acceptance criteria)
       - Expected results
       - Jira reference (key + ID)

3. **Generate AIO Test Case**
   - Transform documentation to AIO API format
   - Execute create_case_by_id.py script with command line arguments:
     ```bash
     python create_case_by_id.py \
       --project "Jira project key"
       --name "Test case name" \
       --description "Test case description" \
       --precondition "Test preconditions" \
       --steps '[{"step":"Step 1","expectedResult":"Expected 1","stepType":"TEXT"},{"step":"Step 2","expectedResult":"Expected 2","stepType":"TEXT"}]' \
       --jira_ids '["jira_id"]'
     ```
   - Required parameters:
     - --name: Test case name (from the generated Markdown file)
     - --steps: JSON array of step objects (step + expectedResult+stepType)
     - --jira_ids: JSON array of Jira requirement IDs
   - Optional parameters:
     - --description: Test case description
     - --precondition: Test preconditions

4. **Verification**
   - Confirm test case creation
   - Validate Jira link
   - Update documentation with AIO test case ID

## Example Command
```bash
python create_case_by_id.py \
  --name "Character Click Feedback" \
  --description "Verify user can login" \
  --precondition "User on Level 1 landing page" \
  --steps '[{"step":"Click the login link","expectedResult":"Load the login page","stepType":"TEXT"}]' \
  --jira_ids '["123456"]'
```

## Example Output
```json
{
  "key": "PROJ-TC-XXX",
  "title": "Character Click Feedback", 
  "status": {"ID": 6, "name": "Under Review"},
  "jiraRequirementIDs": ["216624"]
}
```

## Error Handling
- Handle missing Jira fields
- Validate API responses
- Retry failed requests
- Log errors for debugging
```json
{
  "tool": "jira_get_issue",
  "parameters": {
    "issue_key": "PROJ-123",
    "fields": "id"
  }
}
```

## Error Handling
- Invalid Jira key format
- Ticket not found
- Authentication failures
- Network issues

## Notes
- Works with both standard Jira keys and custom project keys
- Can be chained with other MCP workflows
- Results can be cached for performance

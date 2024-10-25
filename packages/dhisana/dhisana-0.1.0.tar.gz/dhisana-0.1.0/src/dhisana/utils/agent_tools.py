import os
import json
import re
import requests
import uuid
import io
import base64
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from email.mime.text import MIMEText
from typing import Optional, Union, List, Dict, Any
from datetime import datetime, timedelta
from .tools_json import global_assistant_tools
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload, MediaFileUpload

# Read API keys from environment variables
def assistant_tool(func):
    func.is_assistant_tool = True
    return func

@assistant_tool
def search_google_maps(query):
    SERPAPI_API_KEY = os.getenv('SERPAPI_KEY')
    params = {
        'engine': 'google_maps',
        'q': query,
        'num': 20,
        'api_key': SERPAPI_API_KEY
    }
    response = requests.get('https://serpapi.com/search', params=params)
    output =  response.json()
    print(output)
    return output

@assistant_tool
def enrich_people_with_apollo(lead_list):
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    api_url = "https://api.apollo.io/api/v1/people/bulk_match"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    payload = {
        "details": [
            {
                key: lead[key] for key in [
                    "first_name", "last_name", "name", "email", "hashed_email",
                    "organization_name", "domain", "id", "linkedin_url"
                ] if key in lead
            } for lead in lead_list
            if any(lead.get(k) for k in ("first_name", "last_name", "name"))
        ],
        "reveal_personal_emails": True
    }
    
    if not payload["details"]:
        return []
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while enriching data with Apollo.io: {e}")
        return []

@assistant_tool
def search_google(query):
    return _search_serpapi('google', query, 20)

@assistant_tool
def search_google_jobs(query):
    return _search_serpapi('google_jobs', query, 20)

@assistant_tool
def search_google_news(query):
    return _search_serpapi('google_news', query)

def _search_serpapi(engine, query, num=20):
    print(f"Searching {engine.replace('_', ' ').title()} for: {query}")
    SERPAPI_API_KEY = os.getenv('SERPAPI_KEY')
    params = {
        'engine': engine,
        'q': query,
        'num': num,
        'api_key': SERPAPI_API_KEY
    }
    try:
        response = requests.get('https://serpapi.com/search', params=params)
        response.raise_for_status()
        output =  response.json()
        print(output)
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching {engine}: {e}")
        return {}


@assistant_tool
def get_html_content_from_url(url):
    # Check and replace http with https
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"Requesting {url}")
        try:
            page.goto(url, timeout=10000)
            html_content = page.content()
            return parse_html_content(html_content)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return ""
        finally:
            browser.close()

@assistant_tool
def parse_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)

@assistant_tool
def extract_image_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return [{'src': img.get('src'), 'alt': img.get('alt', '')} for img in soup.find_all('img')]

@assistant_tool
def extract_head_section_from_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup.head) if soup.head else ""

@assistant_tool
def get_email_if_exists(website_content):
    email_pattern = r'(mailto:)?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, website_content)
    if match:
        start_index = max(0, match.start() - 7)
        end_index = min(len(website_content), match.end() + 7)
        return website_content[start_index:end_index]
    return ""

@assistant_tool
def search_crunchbase(query):
    api_url = "https://api.crunchbase.com/api/v4/searches/organizations"
    CRUNCHBASE_API_KEY = os.getenv('CRUNCHBASE_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "X-Cb-User-Key": CRUNCHBASE_API_KEY
    }
    payload = {
        "query": {
            "field_id": "organizations.name",
            "operator_id": "contains",
            "value": query
        },
        "field_ids": [
            "identifier", "name", "short_description", "website", "linkedin",
            "twitter", "location_identifiers", "categories", "num_employees_enum",
            "founded_on", "last_funding_type", "last_funding_total"
        ],
        "limit": 5
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching Crunchbase: {e}")
        return {}


@assistant_tool
def search_people_with_apollo(
    person_titles: Optional[Union[str, List[str]]] = None,
    q_keywords: Optional[str] = None,
    person_locations: Optional[Union[str, List[str]]] = None,
    person_seniorities: Optional[Union[str, List[str]]] = None,
    organization_locations: Optional[Union[str, List[str]]] = None,
    organization_num_employees_ranges: Optional[Union[str, List[str]]] = None,
    q_organization_domains: Optional[Union[str, List[str]]] = None,
) -> Dict[str, Any]:
    """
    Search for people on Apollo.io using various filters.

    Args:
        person_titles (str or List[str], optional): Titles of the person to filter by (e.g., ['Sales Manager', 'Engineer', 'Director']).
        q_keywords (str, optional): A string of words over which we want to filter the results (e.g., "Operations Manager, Production Manager").
        person_locations (str or List[str], optional): Locations of the person to filter by (e.g.,  ['California, US', 'Minnesota, US']).
        person_seniorities (str or List[str], optional): Seniorities or levels (e.g., ['manager', 'director', 'ceo']).
        organization_locations (str or List[str], optional): Locations of the organization (e.g., ['Minnesota, US', 'California, US']).
        organization_num_employees_ranges (str or List[str], optional): Employee size ranges of the organization ["101,200", "200,500"]). Default is Empty.
        q_organization_domains (str or List[str], optional): Domains of the organizations to filter by (e.g., ['apollo.io', 'facebook.com']). Organization domain is company domain like facebook.com .
    Returns:
        Dict[str, Any]: The response from Apollo.io containing the search results, or an empty dict on failure.
    """

    api_url = "https://api.apollo.io/v1/mixed_people/search"
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY  # Ensure APOLLO_API_KEY is defined
    }
    payload = {
    }

    if person_titles:
        if isinstance(person_titles, str):
            person_titles = [person_titles]
        payload["person_titles"] = person_titles

    # if q_keywords:
    #     payload["q_keywords"] = q_keywords

    if person_locations:
        if isinstance(person_locations, str):
            person_locations = [person_locations]
        payload["person_locations"] = person_locations

    if person_seniorities:
        if isinstance(person_seniorities, str):
            person_seniorities = [person_seniorities]
        payload["person_seniorities"] = person_seniorities

    if organization_locations:
        if isinstance(organization_locations, str):
            organization_locations = [organization_locations]
        payload["organization_locations"] = organization_locations

    # if organization_num_employees_ranges:
    #     if isinstance(organization_num_employees_ranges, str):
    #         organization_num_employees_ranges = [organization_num_employees_ranges]
    #     payload["organization_num_employees_ranges"] = organization_num_employees_ranges

    if q_organization_domains:
        if isinstance(q_organization_domains, str):
            q_organization_domains = [q_organization_domains]
        # The API expects domains as a newline-separated string
        payload["q_organization_domains"] = '\n'.join(q_organization_domains)

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        output =  response.json()
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching for people on Apollo.io: {e}")
        return {}


@assistant_tool
def search_companies_with_apollo(
    locations: Optional[Union[str, List[str]]] = None,
    industries: Optional[Union[str, List[str]]] = None,
    employee_size_ranges: Optional[Union[str, List[str]]] = None
) -> Dict[str, Any]:
    """
    Search for companies on Apollo.io using various filters.

    Args:
        locations (str or List[str], optional): Locations of the company (city, state, country). (e.g., 'San Jose', ['Seattle', 'New York']).
        industries (str or List[str], optional): Industry sectors of the company. (e.g., 'Manufacturing', ['Bio Medical', 'Defense']).
        employee_size_range (str, optional): Employee size of company to filter by eg (e.g., '50,100', ["1,10", "101,200" ]).

    Returns:
        Dict[str, Any]: The response from Apollo.io containing the search results, or an empty dict on failure.
    """
    api_url = "https://api.apollo.io/api/v1/mixed_companies/search"
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY
    }
    payload = {
        "per_page": 10,
    }
    
    if employee_size_ranges:
        if isinstance(employee_size_ranges, str):
            employee_size_ranges = [employee_size_ranges]
        payload["organization_num_employees_ranges"] = employee_size_ranges

    # Handle location
    if locations:
        if isinstance(locations, str):
            locations = [loc.strip() for loc in locations.split(',')]
        payload["organization_locations"] = locations

    # Handle industry
    if industries:
        if isinstance(industries, str):
            industries = [ind.strip() for ind in industries.split(',')]
        payload["q_organization_keyword_tags"] = industries

    # Note: The API does not support filtering by revenue or funding directly.

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching for companies on Apollo.io: {e}")
        return {}


@assistant_tool
def enrich_company_with_apollo(
    company_domain: str = None,
) -> Dict[str, Any]:
    """
    Enrich company information using Apollo.io.

    Args:
        company_domain (str, optional): The domain of the company (e.g., 'example.com').

    Returns:
        Dict[str, Any]: The enriched company information from Apollo.io, or an empty dict on failure.
    """
    api_url = "https://api.apollo.io/v1/organizations/enrich"
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY 
    }
    
    if not company_domain:
        raise ValueError("company_domain must be provided.")
    params = {"domain": company_domain}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        output =  response.json()
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while enriching company info on Apollo.io: {e}")
        return {}

@assistant_tool
def get_job_postings_from_apollo(
    organization_id: str = None,
) -> List[Dict[str, Any]]:
    """
    Get a list of active job postings for a company using Apollo.io.

    Args:
        organization_id (str, optional): The ID of the organization.

    Returns:
        List[Dict[str, Any]]: The list of job postings from Apollo.io, or an empty list on failure.
    """
    api_url = f"https://api.apollo.io/v1/organizations/{organization_id}/job_postings"
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY  # Ensure you have the API key set up.
    }
    
    if not organization_id:
        raise ValueError("organization_id must be provided.")

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        output = response.json().get("organization_job_postings", [])
        print(output)
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching job postings from Apollo.io: {e}")
        return []


def run_assistant(client, assistant, prompt, response_type, allowed_tools):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )

    allowed_tool_items = [
        tool for tool in global_assistant_tools 
        if tool['type'] == 'function' and tool['function']['name'] in allowed_tools
    ]
    
    response_format = {
        'type': 'json_schema',
        'json_schema': {
            "name": response_type.__class__.__name__,
            "schema": response_type.model_json_schema()
        }
    }

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        response_format=response_format,
        tools=allowed_tool_items,
    )

    max_iterations = 5
    iteration_count = 0

    while run.status == 'requires_action':
        if iteration_count >= max_iterations:
            print("Exceeded maximum number of iterations for requires_action.")
            return "Error: Exceeded maximum number of iterations for requires_action."

        tool_outputs = []
        current_batch_size = 0
        max_batch_size = 256 * 1024

        assistant_tools = {name: func for name, func in globals().items() if callable(func) and getattr(func, 'is_assistant_tool', False)}

        if hasattr(run, 'required_action') and hasattr(run.required_action, 'submit_tool_outputs'):
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool.function.name
                function = assistant_tools.get(function_name)
                if function:
                    try:
                        function_args = json.loads(tool.function.arguments)
                        print(f"Invoking function {function_name} with args: {function_args}")
                        output = function(**function_args)
                        output_str = json.dumps(output)
                        output_size = len(output_str.encode('utf-8'))

                        if current_batch_size + output_size > max_batch_size:
                            tool_outputs.append({"tool_call_id": tool.id, "output": ""})
                        else:
                            tool_outputs.append({"tool_call_id": tool.id, "output": output_str})
                            current_batch_size += output_size
                    except Exception as e:
                        print(f"Error invoking function {function_name}: {e}")
                        tool_outputs.append({"tool_call_id": tool.id, "output": "No results found"})

        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            except Exception as e:
                print("Failed to submit tool outputs:", e)

        iteration_count += 1

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    else:
        return run.status

def extract_and_structure_data(client, assistant, prompt, user_provider_data, response_type, allowed_tools):
    formatted_prompt = prompt.format(input=user_provider_data)
    output = run_assistant(client, assistant, formatted_prompt, response_type, allowed_tools)
    return output


def convert_base_64_json(base64_string):
    """
    Convert a base64 encoded string to a JSON string.

    Args:
        base64_string (str): The base64 encoded string.

    Returns:
        str: The decoded JSON string.
    """
    # Decode the base64 string to bytes
    decoded_bytes = base64.b64decode(base64_string)
    
    # Convert bytes to JSON string
    json_string = decoded_bytes.decode('utf-8')
    
    return json_string

@assistant_tool
def get_file_content_from_googledrive_by_name(file_name: str = None) -> str:
    """
    Searches for a file by name in Google Drive using a service account, downloads it, 
    saves it in /tmp with a unique filename, and returns the local file path.

    :param file_name: The name of the file to search for and download from Google Drive.
    :return: Local file path of the downloaded file.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for Google Drive API access
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account info and impersonate the specific email
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    # Search for the file by name
    query = f"name = '{file_name}'"
    results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        raise FileNotFoundError(f"No file found with the name: {file_name}")
    
    # Get the file ID of the first matching file
    file_id = items[0]['id']
    file_name = items[0]['name']

    # Create a unique filename by appending a UUID to the original file name
    unique_filename = f"{uuid.uuid4()}_{file_name}"

    # Path to save the downloaded file
    local_file_path = os.path.join('/tmp', unique_filename)

    # Request the file content from Google Drive
    request = service.files().get_media(fileId=file_id)
    
    # Create a file-like object in memory to hold the downloaded data
    fh = io.FileIO(local_file_path, 'wb')

    # Initialize the downloader
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    # Close the file handle
    fh.close()

    # Return the local file path
    return local_file_path

@assistant_tool
def write_content_to_googledrive(cloud_file_name: str, local_file_name: str) -> str:
    """
    Writes content from a local file to a file in Google Drive using a service account.
    If the file does not exist in Google Drive, it creates it.
    
    :param cloud_file_name: The name of the file to create or update on Google Drive.
    :param local_file_name: The path to the local file whose content will be uploaded.
    :return: The file ID of the uploaded or updated file.
    """

    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for Google Drive API access
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account info and impersonate the specific email
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    # Check if the file exists in Google Drive
    query = f"name = '{cloud_file_name}'"
    results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    # Prepare the file for upload
    media_body = MediaFileUpload(local_file_name, resumable=True)

    if items:
        # File exists, update its content
        file_id = items[0]['id']
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media_body
        ).execute()
    else:
        # File does not exist, create a new one
        file_metadata = {'name': cloud_file_name}
        created_file = service.files().create(
            body=file_metadata,
            media_body=media_body,
            fields='id'
        ).execute()
        file_id = created_file.get('id')

    return file_id



@assistant_tool
def list_files_in_drive_folder_by_name(folder_name: str = None) -> List[str]:
    """
    Lists all files in the given Google Drive folder by folder name.
    If no folder name is provided, it lists files in the root folder.

    :param folder_name: The name of the folder in Google Drive to list files from.
    :return: A list of file names in the folder.
    :raises Exception: If any error occurs during the process.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for Google Drive API access
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account info and impersonate the specific email
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    folder_id = 'root'  # Default to root if folder_name is None

    if folder_name:
        # Search for the folder by name (assuming unique folder names)
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            raise FileNotFoundError(f"No folder found with the name: {folder_name}")
        
        # Get the folder ID of the first matching folder
        folder_id = items[0]['id']

    # List all files in the specified folder (or root folder if no folder name was provided)
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, pageSize=100, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return []

    # Extract file names
    file_names = [item['name'] for item in items]

    return file_names



@assistant_tool
def send_email_using_service_account(
    recipient: str, subject: str, body: str
) -> str:
    """
    Sends an email using the Gmail API with a service account. 
    The service account must have domain-wide delegation to impersonate the sender.

    :param recipient: The email address of the recipient.
    :param subject: The subject of the email.
    :param body: The body text of the email.
    :return: The ID of the sent message.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for sending email via Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Gmail service object
    service = build('gmail', 'v1', credentials=credentials)

    # Create the email message
    message = MIMEText(body)
    message['to'] = recipient
    message['from'] = email_for_automation
    message['subject'] = subject

    # Encode the message in base64 for sending
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email using the Gmail API
    sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()

    # Return the message ID of the sent email
    return sent_message['id']


@assistant_tool
def get_calendar_events_using_service_account(
    start_date: str, end_date: str
) -> List[Dict[str, Any]]:
    """
    Retrieves a list of events from a user's Google Calendar using a service account.
    The service account must have domain-wide delegation to impersonate the user.
    Events are filtered based on the provided start and end date range.

    :param start_date: The start date (inclusive) to filter events. Format: 'YYYY-MM-DD'.
    :param end_date: The end date (exclusive) to filter events. Format: 'YYYY-MM-DD'.
    :return: A list of calendar events within the specified date range.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required Google Calendar API scope
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Calendar service object
    service = build('calendar', 'v3', credentials=credentials)

    # Convert start and end dates to ISO 8601 format with time (00:00:00) for start and (23:59:59) for end
    start_datetime = f'{start_date}T00:00:00Z'  # UTC format
    end_datetime = f'{end_date}T23:59:59Z'      # UTC format

    # Retrieve the list of events within the date range from the user's primary calendar
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_datetime,
        timeMax=end_datetime,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found within the specified range.')
    else:
        print('Upcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event['summary']}")

    # Return the list of events
    return events

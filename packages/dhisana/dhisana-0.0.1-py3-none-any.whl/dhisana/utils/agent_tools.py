# Global List of tools that can be used in the assistant
# Only functions marked with @assistant_tool will be available in the allowed list
# This is in addition to the tools from OpenAPI Spec add to allowed tools

import os
import json
import re
import aiohttp
import uuid
import io
import base64
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from email.mime.text import MIMEText
from typing import Optional, Union, List, Dict, Any
from .assistant_tool_tag import assistant_tool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import httpx
from google.auth.transport.requests import Request
from typing import List
from googleapiclient.errors import HttpError


GLOBAL_DATA_MODELS = []
GLOBAL_TOOLS_FUNCTIONS = {}

@assistant_tool
async def search_google_maps(query):
    SERPAPI_API_KEY = os.getenv('SERPAPI_KEY')
    params = {
        'engine': 'google_maps',
        'q': query,
        'num': 20,
        'api_key': SERPAPI_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://serpapi.com/search', params=params) as response:
            output = await response.json()
            print(output)
            return output

@assistant_tool
async def enrich_people_with_apollo(lead_list):
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
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error occurred while enriching data with Apollo.io: {e}")
        return []

@assistant_tool
async def search_google(query):
    return await _search_serpapi('google', query, 20)

@assistant_tool
async def search_google_jobs(query):
    return await _search_serpapi('google_jobs', query, 20)

@assistant_tool
async def search_google_news(query):
    return await _search_serpapi('google_news', query)

async def _search_serpapi(engine, query, num=20):
    print(f"Searching {engine.replace('_', ' ').title()} for: {query}")
    SERPAPI_API_KEY = os.getenv('SERPAPI_KEY')
    params = {
        'engine': engine,
        'q': query,
        'num': num,
        'api_key': SERPAPI_API_KEY
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://serpapi.com/search', params=params) as response:
                response.raise_for_status()
                output = await response.json()
                print(output)
                return output
    except aiohttp.ClientError as e:
        print(f"Error occurred while searching {engine}: {e}")
        return {}

@assistant_tool
async def get_html_content_from_url(url):
    # Check and replace http with https
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Requesting {url}")
        try:
            await page.goto(url, timeout=10000)
            html_content = await page.content()
            return await parse_html_content(html_content)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return ""
        finally:
            await browser.close()

@assistant_tool
async def parse_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)

@assistant_tool
async def extract_image_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return [{'src': img.get('src'), 'alt': img.get('alt', '')} for img in soup.find_all('img')]

@assistant_tool
async def extract_head_section_from_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup.head) if soup.head else ""

@assistant_tool
async def get_email_if_exists(website_content):
    email_pattern = r'(mailto:)?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, website_content)
    if match:
        start_index = max(0, match.start() - 7)
        end_index = min(len(website_content), match.end() + 7)
        return website_content[start_index:end_index]
    return ""

@assistant_tool
async def search_crunchbase(query):
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
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error occurred while searching Crunchbase: {e}")
        return {}

@assistant_tool
async def search_people_with_apollo(
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
    payload = {}

    if person_titles:
        if isinstance(person_titles, str):
            person_titles = [person_titles]
        payload["person_titles"] = person_titles

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

    if q_organization_domains:
        if isinstance(q_organization_domains, str):
            q_organization_domains = [q_organization_domains]
        payload["q_organization_domains"] = '\n'.join(q_organization_domains)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                output = await response.json()
                return output
    except aiohttp.ClientError as e:
        print(f"Error occurred while searching for people on Apollo.io: {e}")
        return {}

@assistant_tool
async def search_companies_with_apollo(
    locations: Optional[Union[str, List[str]]] = None,
    industries: Optional[Union[str, List[str]]] = None,
    employee_size_ranges: Optional[Union[str, List[str]]] = None
) -> Dict[str, Any]:
    """
    Search for companies on Apollo.io using various filters.

    Args:
        locations (str or List[str], optional): Locations of the company (city, state, country). (e.g., 'San Jose', ['Seattle', 'New York']).
        industries (str or List[str], optional): Industry sectors of the company. (e.g., 'Manufacturing', ['Bio Medical', 'async defense']).
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

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error occurred while searching for companies on Apollo.io: {e}")
        return {}

@assistant_tool
async def enrich_company_with_apollo(
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
        return ""
    params = {"domain": company_domain}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers, params=params) as response:
                response.raise_for_status()
                output = await response.json()
                return output
    except aiohttp.ClientError as e:
        print(f"Error occurred while enriching company info on Apollo.io: {e}")
        return {}

@assistant_tool
async def get_job_postings_from_apollo(
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
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                response.raise_for_status()
                output = (await response.json()).get("organization_job_postings", [])
                print(output)
                return output
    except aiohttp.ClientError as e:
        print(f"Error occurred while fetching job postings from Apollo.io: {e}")
        return []


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
async def get_file_content_from_googledrive_by_name(file_name: str = None) -> str:
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
async def write_content_to_googledrive(cloud_file_name: str, local_file_name: str) -> str:
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
async def list_files_in_drive_folder_by_name(folder_path: str = None) -> List[str]:
    """
    Lists all files in the given Google Drive folder by folder path.
    If no folder path is provided, it lists files in the root folder.

    :param folder_path: The path of the folder in Google Drive to list files from.
                        Example: '/manda_agent_metadata/openapi_tool_specs/'
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

    folder_id = 'root'  # Start from root if folder_path is None

    if folder_path:
        # Split the folder path into individual folder names
        folder_names = [name for name in folder_path.strip('/').split('/') if name]
        for folder_name in folder_names:
            # Search for the folder by name under the current folder_id
            query = (
                f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' "
                f"and '{folder_id}' in parents and trashed = false"
            )
            try:
                results = service.files().list(
                    q=query,
                    pageSize=1,
                    fields="files(id, name)"
                ).execute()
                items = results.get('files', [])
                if not items:
                    raise FileNotFoundError(
                        f"Folder '{folder_name}' not found under parent folder ID '{folder_id}'"
                    )
                # Update folder_id to the ID of the found folder
                folder_id = items[0]['id']
            except HttpError as error:
                raise Exception(f"An error occurred: {error}")

    # Now folder_id is the ID of the desired folder
    # List all files in the specified folder
    query = f"'{folder_id}' in parents and trashed = false"
    try:
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="files(id, name)"
        ).execute()
        items = results.get('files', [])
        # Extract file names
        file_names = [item['name'] for item in items]
        return file_names
    except HttpError as error:
        raise Exception(f"An error occurred while listing files: {error}")


@assistant_tool
async def send_email_using_service_account_async(
    recipient: str, subject: str, body: str
) -> str:
    """
    Asynchronously sends an email using the Gmail API with a service account.
    The service account must have domain-wide delegation to impersonate the sender.

    :param recipient: The email address of the recipient.
    :param subject: The subject of the email.
    :param body: The body text of the email.
    :return: The ID of the sent message.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')

    if not service_account_base64 or not email_for_automation:
        raise EnvironmentError("Required environment variables are not set.")

    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for sending email via Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Refresh the token if necessary
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    # Get the access token
    access_token = credentials.token

    # Define the Gmail API endpoint for sending messages
    gmail_api_url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'

    # Create the email message
    message = MIMEText(body)
    message['to'] = recipient
    message['from'] = email_for_automation
    message['subject'] = subject

    # Encode the message in base64url format
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Prepare the request payload
    payload = {
        'raw': raw_message
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(gmail_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        sent_message = response.json()

    # Return the message ID of the sent email
    return sent_message.get('id', 'No ID returned')


@assistant_tool
async def get_calendar_events_using_service_account_async(
    start_date: str, end_date: str
) -> List[Dict[str, Any]]:
    """
    Asynchronously retrieves a list of events from a user's Google Calendar using a service account.
    The service account must have domain-wide delegation to impersonate the user.
    Events are filtered based on the provided start and end date range.

    :param start_date: The start date (inclusive) to filter events. Format: 'YYYY-MM-DD'.
    :param end_date: The end date (exclusive) to filter events. Format: 'YYYY-MM-DD'.
    :return: A list of calendar events within the specified date range.
    """
    # Helper function to decode base64 JSON
    def convert_base_64_json(encoded_json: str) -> str:
        decoded_bytes = base64.b64decode(encoded_json)
        return decoded_bytes.decode('utf-8')

    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')

    if not email_for_automation or not service_account_base64:
        raise EnvironmentError("Required environment variables are not set.")

    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required Google Calendar API scope
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Refresh the token if necessary
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    # Get the access token
    access_token = credentials.token

    # Define the API endpoint
    calendar_api_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

    # Convert start and end dates to ISO 8601 format with time
    start_datetime = f'{start_date}T00:00:00Z'  # UTC format
    end_datetime = f'{end_date}T23:59:59Z'      # UTC format

    params = {
        'timeMin': start_datetime,
        'timeMax': end_datetime,
        'maxResults': 10,
        'singleEvents': True,
        'orderBy': 'startTime'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(calendar_api_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        events_result = response.json()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found within the specified range.')
    else:
        print('Upcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event.get('summary', 'No Title')}")

    return events

GLOBAL_TOOLS_FUNCTIONS = {name: func for name, func in globals().items() if callable(func) and getattr(func, 'is_assistant_tool', False)}
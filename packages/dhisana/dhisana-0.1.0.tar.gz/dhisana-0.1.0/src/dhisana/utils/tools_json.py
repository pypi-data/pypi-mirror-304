global_assistant_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_google_maps",
            "description": "Search for locations on Google Maps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g., 'restaurants in New York'."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "enrich_company_with_apollo",
            "description": "Enrich company information with information in apollo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_domain": {
                        "type": "string",
                        "description": "website domain of the company'."
                    }
                },
                "required": ["company_domain"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_job_postings_from_apollo",
            "description": "Get a list of active job postings for a company using Apollo.io.",
            "parameters": {
                "type": "object",
                "properties": {
                    "organization_id": {
                        "type": "string",
                        "description": "The ID of the organization."
                    }
                },
                "required": ["organization_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_companies_with_apollo",
            "description": "Search for companies on Apollo.io using various filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "locations": {
                        "anyOf": [
                            { "type": "string" },
                            { "type": "array", "items": { "type": "string" } }
                        ],
                        "description": "Locations to filter by. (e.g., 'San Jose', ['Seattle', 'New York'])"
                    },
                    "industries": {
                        "anyOf": [
                            { "type": "string" },
                            { "type": "array", "items": { "type": "string" } }
                        ],
                        "description": "Industry sectors to filter by. (e.g., 'Manufacturing', ['Bio Medical', 'Defense'])"
                    },
                    "employee_size_ranges": {
                        "anyOf": [
                            { "type": "string" },
                            { "type": "array", "items": { "type": "string" } }
                        ],
                        "description": "Employee size of company to filter by eg (e.g., '50,100', ['1,10', '101,200' ])."
                    },
                },
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "enrich_people_with_apollo",
            "description": "Enrich a list of people's information using Apollo.io.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "first_name": {
                                    "type": "string",
                                    "description": "The person's first name."
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "The person's last name."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "The person's full name."
                                },
                                "email": {
                                    "type": "string",
                                    "description": "The person's email address."
                                },
                                "hashed_email": {
                                    "type": "string",
                                    "description": "The hashed email of the person."
                                },
                                "organization_name": {
                                    "type": "string",
                                    "description": "The person's organization name."
                                },
                                "domain": {
                                    "type": "string",
                                    "description": "The organization's domain name."
                                },
                                "id": {
                                    "type": "string",
                                    "description": "The person's unique identifier."
                                },
                                "linkedin_url": {
                                    "type": "string",
                                    "description": "The person's LinkedIn URL."
                                }
                            },
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["lead_list"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_google",
            "description": "Search for information on Google Search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g., 'weather tomorrow'."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_google_jobs",
            "description": "Search for jobs on Google Jobs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g., 'software engineer jobs in San Francisco'."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_google_news",
            "description": "Search for news articles on Google News.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g., 'latest tech news'."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_html_content_from_url",
            "description": "Retrieve the HTML content from a given URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the webpage to fetch."
                    }
                },
                "required": ["url"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "parse_html_content",
            "description": "Parse HTML content and extract text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_content": {
                        "type": "string",
                        "description": "The HTML content to parse."
                    }
                },
                "required": ["html_content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_image_links",
            "description": "Extract image links from HTML content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_content": {
                        "type": "string",
                        "description": "The HTML content to parse."
                    }
                },
                "required": ["html_content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_head_section_from_html_content",
            "description": "Extract the <head> section from HTML content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_content": {
                        "type": "string",
                        "description": "The HTML content to parse."
                    }
                },
                "required": ["html_content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_email_if_exists",
            "description": "Extract an email address if it exists in the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "website_content": {
                        "type": "string",
                        "description": "The text content to search for an email address."
                    }
                },
                "required": ["website_content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_crunchbase",
            "description": "Search for organizations on Crunchbase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The organization name to search for."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_people_with_apollo",
            "description": "Search for people on Apollo.io using various filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_titles": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Titles of the person to filter by (e.g., ['Sales Manager', 'Engineer', 'Director'])."
                    },
                    "q_keywords": {
                        "type": "string",
                        "description": "A string of words over which we want to filter the results (e.g., 'Operations Manager, Production Manager')."
                    },
                    "person_locations": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Locations of the person to filter by (e.g., ['California, US', 'Minnesota, US'])."
                    },
                    "person_seniorities": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Seniorities or levels (e.g., ['manager', 'director', 'ceo'])."
                    },
                    "organization_locations": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Locations of the organization (e.g., ['Minnesota, US', 'California, US'])."
                    },
                    "organization_num_employees_ranges": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Employee size ranges of the organization (e.g., ['101,200', '200,500'])."
                    },
                    "q_organization_domains": {
                        "type": ["string", "array"],
                        "items": {
                            "type": "string"
                        },
                        "description": "Domains of the organizations to filter by (e.g., ['apollo.io', 'facebook.com']). Organization domain is company domain like facebook.com."
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_content_from_googledrive_by_name",
            "description": "Searches for a file by name in Google Drive using a service account, downloads it, saves it with a unique filename, and returns the local file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to search for and download from Google Drive."
                    }
                },
                "required": ["file_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email_using_service_account",
            "description": "Sends an email using the Gmail API with a service account. The service account must have domain-wide delegation to impersonate the sender.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "string",
                        "description": "The email address of the sender (must be a user in the domain)."
                    },
                    "recipient": {
                        "type": "string",
                        "description": "The email address of the recipient."
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email."
                    },
                    "body": {
                        "type": "string",
                        "description": "The body text of the email."
                    }
                },
                "required": ["sender", "recipient", "subject", "body"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events_using_service_account",
            "description": "Retrieves a list of events from a user's Google Calendar using a service account. Events are filtered based on the provided start and end date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "The email address of the user whose calendar events are to be retrieved."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The start date (inclusive) to filter events. Format: 'YYYY-MM-DD'."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date (exclusive) to filter events. Format: 'YYYY-MM-DD'."
                    }
                },
                "required": ["user_email", "start_date", "end_date"],
                "additionalProperties": False
            }
        }
    }
]

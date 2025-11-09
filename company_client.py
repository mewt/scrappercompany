import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import re
import time 

# --- Configuration Constants ---
SEARCH_BASE_URL = "https://companieshouse.id/search?term="
BASE_DOMAIN = "https://companieshouse.id"

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Accept": "text/html",
}

# Fields to extract from the detail page
TARGET_FIELDS = [
    "Registered name",
    "Legal entity type",
    "Business number",
    "Registered address",
    "City"
]

# --- Helper Function for Flexible Matching ---

def standardize_name(name):
    """
    Removes periods, commas, converts to lowercase, and strips whitespace 
    to allow for flexible matching between user input and link text.
    """
    # Remove all periods and commas, then strip whitespace and convert to lowercase
    return name.replace('.', '').replace(',', '').strip().lower()

# --- Scraping Functions ---

def scrape_detail_page(detail_url):
    """
    Fetches and scrapes the company details from a specific profile page URL 
    using robust HTML sibling traversal logic.
    """
    print(f"  --> Fetching detail page: {detail_url}")
    
    try:
        # Rate Limiting: Pause for 1 second before making the request
        time.sleep(1) 
        response = requests.get(detail_url, headers=HEADERS, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        
        extracted_data = {}
        
        for field_name in TARGET_FIELDS:
            
            # 1. Find the <h3> tag that holds the label text
            label_h3 = soup.find('h3', string=field_name)
            
            if label_h3:
                # 2. Get the immediate parent div of the <h3> (the label container)
                label_parent_div = label_h3.parent 
                
                # 3. Find the value div by looking for the next sibling of the label container
                value_container = label_parent_div.find_next_sibling('div')
                
                if value_container:
                    # Get the clean text from the value container
                    value = value_container.get_text(strip=True)
                    extracted_data[field_name] = value
                else:
                    extracted_data[field_name] = f"Value container not found using sibling traversal for {field_name}"
            else:
                extracted_data[field_name] = f"Label not found for {field_name}"
                
        # Check for successful extraction
        if any("not found" not in v.lower() for v in extracted_data.values()):
             return extracted_data
             
        return None 

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the detail request to {detail_url}: {e}")
        return None


def extract_company_data(company_name):
    """
    Performs the two-step scrape: Search -> Find Link -> Scrape Detail Page.
    Uses standardized comparison for reliable link matching.
    """
    search_url = SEARCH_BASE_URL + quote_plus(company_name)
    print(f"1. Fetching search results URL: {search_url}")
    
    # Standardize the input name for a loose comparison
    standardized_input_name = standardize_name(company_name)

    try:
        # --- Step 1: Find the Detail Link from the Search Results ---
        # Rate Limiting: Pause for 1 second before making the search request
        time.sleep(1) 
        search_response = requests.get(search_url, headers=HEADERS, timeout=10)
        search_response.raise_for_status() 
        search_soup = BeautifulSoup(search_response.content, 'html.parser')
        
        # Target the <a> tag by comparing the standardized input name to the standardized link text
        target_link = search_soup.find('a', 
            string=lambda t: t and standardized_input_name == standardize_name(t)
        )
        
        if not target_link:
            print(f"Company '{company_name}' not found as a standardized match in the search results.")
            return None
            
        relative_url = target_link.get('href')
        
        if not relative_url:
             print("Found company name but link (href) was missing.")
             return None
             
        # Create the absolute URL for the detail page
        detail_page_url = urljoin(BASE_DOMAIN, relative_url)
        
        # --- Step 2: Scrape the Detail Page ---
        return scrape_detail_page(detail_page_url)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the search request: {e}")
        return None

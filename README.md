# Company Scraper API

A Flask-based web API that scrapes company information from companieshouse.id.

## Overview

This project provides a simple API that allows you to search for Indonesian company information by name. It uses web scraping techniques to retrieve data from companieshouse.id and returns it in a structured JSON format.

## Features

- RESTful API endpoint to search for company data
- Extracts key company information including registered name, legal entity type, business number, address, and city
- Handles error cases when a company is not found
- Standardized name matching for more flexible searching

## Files

- `app.py`: Main Flask application with the API endpoint
- `company_client.py`: Web scraping logic for extracting company data
- `.gitignore`: Specifies files and directories to ignore in git

## Usage

To run the Flask application locally:

```bash
python app.py
```

Then make a GET request to:

```
http://localhost:5000/company/search?name=PT.%20Buka%20Bumi%20Konstruksi
```

## API Endpoint

`GET /company/search?name={company_name}`

- `name`: The name of the company to search for

Returns a JSON object with company information or an error message if not found.

## Dependencies

This project uses:
- Flask: for the web API framework
- requests: for making HTTP requests
- BeautifulSoup: for parsing HTML content
- time: for rate limiting

## Note

This project implements rate limiting to be respectful to the target website. Please use responsibly and comply with the target website's terms of service.
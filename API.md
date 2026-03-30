# Company Scraper API Documentation

## Overview

This is a Flask-based API that scrapes Indonesian company information from [companieshouse.id](https://companieshouse.id).

## API Specification

The complete API specification is available in [Swagger/OpenAPI format](./swagger.json).

You can view it using:
- [Swagger Editor](https://editor.swagger.io/) - Paste the swagger.json content
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Host it locally

## Quick Start

### Installation

```bash
# Install dependencies
pip install flask requests beautifulsoup4

# Run the application
python app.py
```

### API Endpoints

#### Search Company

```http
GET /company/search?name={company_name}
```

**Parameters:**
- `name` (required): Company name to search for

**Example Request:**
```bash
curl "http://localhost:5000/company/search?name=PT.%20Buka%20Bumi%20Konstruksi"
```

**Example Response:**
```json
{
  "Registered Name": "PT. Buka Bumi Konstruksi",
  "Legal Entity Type": "Limited Liability Company",
  "Business Number": "1218057",
  "Registered Address": "Gold Coast Office Tower Liberty Lantai 3 GH, Jalan Pantai Indah Kapuk",
  "City": "NORTH JAKARTA"
}
```

## Error Responses

| Status Code | Description | Example Response |
|------------|-------------|------------------|
| 400 | Missing parameter | `{"error": "Missing 'name' parameter"}` |
| 503 | Company not found | `{"error": "Could not find information for 'Company'"}` |

## Response Fields

| Field | Description | Example |
|-------|-------------|---------|
| Registered Name | Official company name | "PT. Buka Bumi Konstruksi" |
| Legal Entity Type | Company type | "Limited Liability Company" |
| Business Number | Registration number | "1218057" |
| Registered Address | Official address | "Gold Coast Office Tower..." |
| City | Registration city | "NORTH JAKARTA" |

## Name Matching

The API uses standardized name matching that:
- Removes periods (.) and commas (,)
- Converts to lowercase
- Trims whitespace

This allows flexible searches like:
- `PT. Buka Bumi Konstruksi`
- `PT Buka Bumi Konstruksi`
- `PT., Buka Bumi Konstruksi`

All match the same company.

## Rate Limiting

The API implements a 1-second delay between requests to be respectful to the source website.

## Source

Data is scraped from [companieshouse.id](https://companieshouse.id) for educational purposes.
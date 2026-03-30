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

## API Endpoints

### 1. Health Check

Check if the API service is running.

```http
GET /health
```

**Example Request:**
```bash
curl "http://localhost:5000/health"
```

**Example Response:**
```json
{
  "status": "healthy"
}
```

**Use Case:** Monitoring, load balancer health checks

---

### 2. Check Company Exists (Lightweight)

Quick check to verify if a company exists **without** scraping full details. Much faster than `/company/search` (2-5 seconds vs 30+ seconds).

```http
GET /company/check?name={company_name}
```

**Parameters:**
- `name` (required): Company name to check

**Example Request:**
```bash
curl "http://localhost:5000/company/check?name=PT.%20Buka%20Bumi%20Konstruksi"
```

**Success Response (200):**
```json
{
  "exists": true,
  "name": "PT. Buka Bumi Konstruksi",
  "url": "https://companieshouse.id/buka-bumi-konstruksi"
}
```

**Not Found Response (404):**
```json
{
  "exists": false
}
```

**Use Case:** 
- Pre-validation before full extraction
- CRM workflows (check before adding to database)
- Quick availability checks

---

### 3. Search Company (Full Extraction)

Full company search with complete data extraction from the detail page.

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

**Use Case:** When you need complete company details

---

## Error Responses

| Status Code | Endpoint | Description | Example Response |
|------------|----------|-------------|------------------|
| 200 | All | Success | Varies by endpoint |
| 400 | `/company/check`, `/company/search` | Missing parameter | `{"error": "Missing 'name' parameter"}` |
| 404 | `/company/check` | Company not found | `{"exists": false}` |
| 503 | `/company/search` | Company not found or extraction failed | `{"error": "Could not find information for 'Company'"}` |

## Response Fields

### Company Check Response

| Field | Description | Example |
|-------|-------------|---------|
| exists | Whether company was found | `true` or `false` |
| name | Official company name | "PT. Buka Bumi Konstruksi" |
| url | Detail page URL | "https://companieshouse.id/buka-bumi-konstruksi" |

### Company Search Response

| Field | Description | Example |
|-------|-------------|---------|
| Registered Name | Official company name | "PT. Buka Bumi Konstruksi" |
| Legal Entity Type | Company type | "Limited Liability Company" |
| Business Number | Registration number | "1218057" |
| Registered Address | Official address | "Gold Coast Office Tower..." |
| City | Registration city | "NORTH JAKARTA" |

## Workflow Example

### For CRM Integration (Pipedream, Zapier, etc.)

```javascript
// Step 1: Check if company exists (fast)
const checkResponse = await $http({
  url: "http://localhost:5000/company/check",
  params: { name: "PT Example Company" }
});

// Step 2: Only extract full data if company exists
if (checkResponse.status === 200 && checkResponse.data.exists) {
  // Company exists, get full details
  const fullData = await $http({
    url: "http://localhost:5000/company/search",
    params: { name: "PT Example Company" }
  });
  
  // Add to your CRM
  console.log("Adding to CRM:", fullData.data);
} else {
  // Skip - company not found
  console.log("Company not found, skipping...");
}
```

**Benefits:**
- Saves time by avoiding full extraction for non-existent companies
- Reduces load on the source website
- Faster workflow execution

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

## Performance Comparison

| Endpoint | Average Response Time | Use Case |
|----------|---------------------|----------|
| `/health` | < 100ms | Monitoring |
| `/company/check` | 2-5 seconds | Existence verification |
| `/company/search` | 30-60 seconds | Full data extraction |

## Source

Data is scraped from [companieshouse.id](https://companieshouse.id) for educational purposes.
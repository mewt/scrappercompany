from flask import Flask, jsonify, request
from company_client import extract_company_data # Import the scraper function

app = Flask(__name__)

# Define the API endpoint
@app.route('/company/search', methods=['GET'])
def search_company():
    """
    API endpoint to search for company data.
    Usage: GET /company/search?name=PT.%20Buka%20Bumi%20Konstruksi
    """
    
    # Get the company name dynamically from the URL query string
    company_name = request.args.get('name')
    
    # Validate input
    if not company_name:
        return jsonify({"error": "Missing 'name' parameter in the request."}), 400

    # Call the scraper function with the dynamic input
    company_info = extract_company_data(company_name)
    
    # Handle success or failure
    if company_info is None:
        return jsonify({"error": f"Could not find or extract information for '{company_name}'. Please verify the company name."}), 503
        
    # Return the extracted data as JSON
    return jsonify(company_info)

if __name__ == '__main__':
    print("Starting Flask API server...")
    # Run in debug mode for development
    app.run(debug=True)

from flask import Flask, jsonify, request
from company_client import extract_company_data, check_company_exists

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/company/check', methods=['GET'])
def check_company():
    """
    Lightweight check if company exists.
    Returns: 200 if found, 404 if not found
    """
    company_name = request.args.get('name')
    if not company_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    result = check_company_exists(company_name)
    if result is None:
        return jsonify({"exists": False}), 404
    return jsonify(result), 200

@app.route('/company/search', methods=['GET'])
def search_company():
    """Full company search with data extraction."""
    company_name = request.args.get('name')
    if not company_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    company_info = extract_company_data(company_name)
    if company_info is None:
        return jsonify({"error": f"Could not find company '{company_name}'"}), 503
    return jsonify(company_info)

if __name__ == '__main__':
    print("Starting Flask API server...")
    app.run(debug=True)
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
import os
from dotenv import load_dotenv
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products  
from flask_cors import CORS  # Add CORS support

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
load_dotenv()

# Configure Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,  # Change for development/production
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# In-memory storage for access token (use database in production)
access_token = None #"access-sandbox-9410dad6-5f36-4951-9f75-2f405497e124"

@app.route('/create_sandbox_token', methods=['POST'])
def create_sandbox_public_token():
    """
    Creates a sandbox public token for testing
    Requires JSON payload:
    {
        "institution_id": "ins_1",
        "products": ["transactions"]  # Must be valid product strings
    }
    """
    try:
        data = request.json
        
        # Convert string product names to Product enums
        products = [Products(product) for product in data.get('products', ['transactions'])]
        
        req = SandboxPublicTokenCreateRequest(
            institution_id=data.get('institution_id', 'ins_1'),
            initial_products=products,  # Use the converted products list
            options={}
        )
        
        response = client.sandbox_public_token_create(req)
        return jsonify({
            'public_token': response.public_token,
            'request_id': response.request_id
        })
        
    except ValueError as e:
        return jsonify({'error': f"Invalid product name: {str(e)}"}), 400
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    try:
        # Create link token
        request = {
            'user': {
                'client_user_id': 'unique-user-id',
            },
            'client_name': 'My App',
            'products': ['transactions'],
            'country_codes': ['US'],
            'language': 'en',
        }
        response = client.link_token_create(request)
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400

@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    global access_token
    try:
        public_token = request.json['public_token']
        response = client.item_public_token_exchange({'public_token': public_token})
        access_token = response['access_token']
        return jsonify({'message': 'Access token stored successfully', 'access_token': access_token})
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400
    except KeyError:
        return jsonify({'error': 'Missing public token'}), 400

@app.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        # Get parameters from request
        access_token = request.args.get('access_token')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Validate required parameters
        if not access_token:
            return jsonify({'error': 'Missing required access_token parameter'}), 400

        # Set date defaults (last 30 days if not specified)
        end_date = datetime.now().date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        start_date = end_date - timedelta(days=30)
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        # Validate date order
        if start_date > end_date:
            return jsonify({'error': 'start_date cannot be after end_date'}), 400

        # Create and execute request
        request_obj = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = client.transactions_get(request_obj)
        
        return jsonify(response.to_dict())
    
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200, debug=True)
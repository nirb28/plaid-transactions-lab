import requests
import json

BASE_URL = 'http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200'  # Adjust the base URL as needed

def create_sandbox_token(institution_id, products):
    url = f"{BASE_URL}/create_sandbox_token"
    payload = {
        "institution_id": institution_id,
        "products": products
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def exchange_public_token(public_token):
    url = f"{BASE_URL}/exchange_public_token"
    payload = {
        "public_token": public_token
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def get_transactions(access_token, start_date, end_date):
    url = f"{BASE_URL}/transactions"
    params = {
        "access_token": access_token,
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(url, params=params)
    return response.json()

def perform_sequence():
    # Step 1: Create sandbox token
    sandbox_token_response = create_sandbox_token("ins_1", ["transactions"])
    public_token = sandbox_token_response.get('public_token')
    print("Sandbox Token Response:", sandbox_token_response)

    # Step 2: Exchange the public token for access token
    exchange_response = exchange_public_token(public_token)
    access_token = exchange_response.get('access_token')
    print("Exchange Public Token Response:", exchange_response)

    # Step 3: Call transactions endpoint
    transactions_response = get_transactions(access_token, "2024-01-01", "2024-01-31")
    print("Transactions Response:", transactions_response)

if __name__ == "__main__":
    #perform_sequence()
    access_token = "access-sandbox-9f5f0999-37ef-4036-b9ba-9bbd7940bbcb"
    transactions_response = get_transactions(access_token, "2024-01-01", "2024-01-31")
    print("Transactions Response:", transactions_response)

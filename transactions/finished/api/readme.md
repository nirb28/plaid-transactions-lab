To run:

cd transactions/finished/api/
flask run --host=0.0.0.0 --port=3200

To use this:

Step 1: create sandbox token (ins_3 is Bank of America, ins_1 is Wells Fargo)
curl -X POST http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/create_sandbox_token \
  -H "Content-Type: application/json" \
  -d '{"institution_id": "ins_1", "products": ["transactions"]}'

> Gives public token for step 2

Step 2: Exchange the public token for access token:
curl -X POST http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/exchange_public_token \
  -H "Content-Type: application/json" \
  -d '{"public_token": "public-sandbox-3a50b222-ba6f-4a5d-a236-efcfa42111dc"}'

Step 3: Call transactions endpoint
http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/transactions?access_token=access-sandbox-2738b32d-ed8b-4e31-97a1-8be3bec13b8f&start_date=2024-01-01&end_date=2024-01-31

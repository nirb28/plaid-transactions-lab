To run:
cd transactions/finished/api/
(plaid) azureuser@vm-ds-ubuntu22:~/workspace/git/plaid-transactions-lab/transactions/finished/api$ flask run --host=0.0.0.0 --port=3200

To use this:

Step 1: create sandbox token
curl -X POST http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/create_sandbox_token \
  -H "Content-Type: application/json" \
  -d '{"institution_id": "ins_1", "products": ["transactions"]}'

> Gives public token for step 2

Step 2: Exchange the public token for access token:
curl -X POST http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/exchange_public_token \
  -H "Content-Type: application/json" \
  -d '{"public_token": "public-sandbox-3cefda87-4106-440d-98a2-d2e02d9d8920"}'

Step 3: Call transactions endpoint
http://vm-ds-ubuntu22.eastus2.cloudapp.azure.com:3200/transactions?access_token=your_token&start_date=2024-01-01&end_date=2024-01-31

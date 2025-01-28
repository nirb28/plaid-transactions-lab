To use this:

Step 1: create sandbox token
curl -X POST http://localhost:5000/create_sandbox_token \
  -H "Content-Type: application/json" \
  -d '{"institution_id": "ins_1", "products": ["transactions"]}'

> Gives public token for step 2

Step 2: Exchange the public token for access token:
curl -X POST http://localhost:5000/exchange_public_token \
  -H "Content-Type: application/json" \
  -d '{"public_token": "public-sandbox-..."}'

Step 3: Call transactions endpoint
curl "http://localhost:5000/transactions?access_token=your_token&start_date=2024-01-01&end_date=2024-01-31"

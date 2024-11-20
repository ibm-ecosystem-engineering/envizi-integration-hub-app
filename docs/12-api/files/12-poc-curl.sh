curl --location 'http://localhost:3001/api/push/poc' \
--header 'Content-Type: application/json' \
--data '[{
    "Organization": "IBM APAC",
    "Location": "G50-Loc1",
    "Account Style Caption": "S3.6 - Hotel Stays - Room nights",
    "Account Number": "G50-Loc1-HotelStays",
    "Account Supplier": "Hub",
    "Record Start YYYY-MM-DD": "2024-01-01",
    "Record End YYYY-MM-DD": "2024-03-31",
    "Quantity": 100
}]'
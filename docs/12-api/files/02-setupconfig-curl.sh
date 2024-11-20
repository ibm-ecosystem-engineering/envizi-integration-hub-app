
curl --location 'http://localhost:3001/api/push/setupConfig' \
--header 'Content-Type: application/json' \
--data '[{
    "ORGANIZATION": "IBM APAC",
    "GROUP TYPE": "Classification",
    "GROUP NAME 1": "G50-Group1",
    "GROUP NAME 2": "G50-Group2",
    "GROUP NAME 3": "G50-Group3",

    "LOCATION": "G50-Loc1",
    "CITY": "Chennai",
    "COUNTRY": "India"
}]'
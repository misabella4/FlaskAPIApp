# FlaskAPIApp

This project is a Flask API that returns the current local time of a world capital city.

# API Details
- IP Address: 34.69.215.169
- Port: 5001
- URL: http://34.69.215.169:5001

# How to Use

Call the API:
Open a terminal and run the following command, replacing {city} with your chosen world capital:

curl -H "Authorization: Bearer supersecrettoken123" http://34.69.215.169:5001/api/current-time/{city}

For example:
curl -H "Authorization: Bearer supersecrettoken123" http://34.69.215.169:5001/api/current-time/madrid

Response:
The API will return the current local time for the specified capital city in the following format:

{
  "abbreviation": "CET",
  "city": "Madrid",
  "local_time": "2025-04-22 01:08:14",
  "utc_offset": "UTC+01:00"
}

# Requirements
- Python
- Flask

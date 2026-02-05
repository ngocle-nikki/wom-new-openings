import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GOOGLE_PLACES_API_KEY")

if not key:
    print("Missing GOOGLE_PLACES_API_KEY in .env")
    raise SystemExit(1)

url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {"query": "new restaurant Helsinki", "key": key}

r = requests.get(url, params=params, timeout=30)
data = r.json()

print("API status:", data.get("status"))
if data.get("error_message"):
    print("error_message:", data["error_message"])

for x in data.get("results", [])[:3]:
    print("-", x.get("name"), "|", x.get("formatted_address"))


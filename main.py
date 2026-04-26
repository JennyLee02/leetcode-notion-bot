import os
import requests

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text[:500])

import os
import requests
//
NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

response = requests.post(url, headers=headers)
data = response.json()

print("Status:", response.status_code)

for page in data["results"]:
    properties = page["properties"]
    name_property = properties["Name"]["title"]

    if name_property:
        problem_name = name_property[0]["plain_text"]
        print("Problem:", problem_name)

import os
import requests
from datetime import datetime

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

today = datetime.now().date()

print("Status:", response.status_code)
print("\nReview Problems:")

for page in data["results"]:
    properties = page["properties"]

    name_property = properties["Problem"]["title"]
    if not name_property:
        continue

    problem_name = name_property[0]["plain_text"]
    next_review = properties["Next Review"]["date"]

    if next_review:
        review_date = next_review["start"][:10]

        if review_date <= str(today):
            print("-", problem_name)

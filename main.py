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

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data["results"]

def get_review_problems(pages):
    today = str(datetime.now().date())
    review = []

    for page in pages:
        props = page["properties"]
        name_prop = props["Problem"]["title"]

        if not name_prop:
            continue

        name = name_prop[0]["plain_text"]
        page_id = page["id"]
        next_review = props["Next Review"]["date"]

        if next_review:
            review_date = next_review["start"][:10]

            if review_date <= today:
                review.append({
                    "name": name,
                    "page_id": page_id
                })

    return review

def get_new_problems(pages, limit=3):
    new = []

    for page in pages:
        props = page["properties"]
        name_prop = props["Problem"]["title"]

        if not name_prop:
            continue

        name = name_prop[0]["plain_text"]
        status = props["Status"]["select"]

        if status and status["name"] == "Not Started":
            new.append(name)

        if len(new) >= limit:
            break

    return new

pages = get_pages()
review = get_review_problems(pages)
new = get_new_problems(pages)

print("\n==============================")
print("TODAY'S LEETCODE PLAN")
print("==============================")

print("\n🔁 Review:")
if review:
    for problem in review:
        print("-", problem["name"])
else:
    print("None 🎉")

print("\n🆕 New:")
if new:
    for problem in new:
        print("-", problem)
else:
    print("None")

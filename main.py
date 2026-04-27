import os
import requests
from datetime import datetime, timedelta

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
    return response.json()["results"]

def update_next_review(page_id, days):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    next_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    payload = {
        "properties": {
            "Next Review": {
                "date": {
                    "start": next_date
                }
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    print("Updated review date:", next_date, "status:", response.status_code)

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
                    "page_id": page_id,
                    "props": props
                })

    return review

def get_new_problems(pages, review_names, limit=3):
    new = []

    for page in pages:
        props = page["properties"]
        name_prop = props["Problem"]["title"]

        if not name_prop:
            continue

        name = name_prop[0]["plain_text"]

        if name in review_names:
            continue

        status = props["Status"]["select"]

        if status and status["name"] == "Not Started":
            new.append(name)

        if len(new) >= limit:
            break

    return new

def process_reviews(review):
    for item in review:
        props = item["props"]
        page_id = item["page_id"]

        confidence_prop = props["Confidence"]["number"]

        if confidence_prop is None:
            continue

        confidence = int(confidence_prop)

        if confidence <= 2:
            update_next_review(page_id, 1)
        elif confidence == 3:
            update_next_review(page_id, 2)
        elif confidence == 4:
            update_next_review(page_id, 5)
        elif confidence >= 5:
            update_next_review(page_id, 7)

pages = get_pages()
review = get_review_problems(pages)

review_names = set([r["name"] for r in review])

# 🔥 Update next review dates
process_reviews(review)

new = get_new_problems(pages, review_names)

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

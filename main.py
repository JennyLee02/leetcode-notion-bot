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

# ---------------- API ----------------

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
                "date": {"start": next_date}
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    print("Updated review date:", next_date, "status:", response.status_code)

# ---------------- REVIEW ----------------

def get_due_reviews(pages):
    today = str(datetime.now().date())
    due = []

    for page in pages:
        props = page["properties"]
        name_prop = props["Problem"]["title"]

        if not name_prop:
            continue

        next_review = props["Next Review"]["date"]

        if next_review:
            review_date = next_review["start"][:10]

            if review_date <= today:
                due.append({
                    "name": name_prop[0]["plain_text"],
                    "page_id": page["id"],
                    "props": props
                })

    return due

def process_reviews(due_reviews):
    for item in due_reviews:
        confidence = item["props"]["Confidence"]["number"]

        if confidence is None:
            continue

        confidence = int(confidence)

        if confidence <= 2:
            update_next_review(item["page_id"], 1)
        elif confidence == 3:
            update_next_review(item["page_id"], 2)
        elif confidence == 4:
            update_next_review(item["page_id"], 5)
        elif confidence >= 5:
            update_next_review(item["page_id"], 7)

# ---------------- NEW SELECTION ----------------

def get_new_problems(pages, review_names):
    easy, medium, hard = [], [], []

    for page in pages:
        props = page["properties"]
        name_prop = props["Problem"]["title"]

        if not name_prop:
            continue

        name = name_prop[0]["plain_text"]

        if name in review_names:
            continue

        status = props["Status"]["select"]
        difficulty = props["Difficulty"]["select"]

        if not status or status["name"] != "Not Started":
            continue

        if not difficulty:
            continue

        diff = difficulty["name"]

        if diff == "Easy":
            easy.append(name)
        elif diff == "Medium":
            medium.append(name)
        elif diff == "Hard":
            hard.append(name)

    selected = []

    # 1 easy
    if easy:
        selected.append(easy[0])

    # 2 medium
    selected.extend(medium[:2])

    # 0-1 hard
    if hard:
        selected.append(hard[0])

    return selected

# ---------------- MAIN FLOW ----------------

# 1. Fetch
pages = get_pages()

# 2. Find due reviews
due_reviews = get_due_reviews(pages)

# 3. Update review schedule
process_reviews(due_reviews)

# 4. Refresh after updates
pages = get_pages()

# 5. Final review list (limit 3)
review = get_due_reviews(pages)[:3]

review_names = set([r["name"] for r in review])

# 6. New selection
new = get_new_problems(pages, review_names)

# ---------------- OUTPUT ----------------

print("\n==============================")
print("TODAY'S LEETCODE PLAN")
print("==============================")

print("\n🔁 Review (max 3):")
if review:
    for problem in review:
        print("-", problem["name"])
else:
    print("None 🎉")

print("\n🆕 New (1 Easy, 2 Medium, 0-1 Hard):")
if new:
    for problem in new:
        print("-", problem)
else:
    print("None")

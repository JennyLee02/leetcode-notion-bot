import os
import requests
from datetime import datetime, timedelta
from collections import Counter

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

# ---------------- HELPERS ----------------

def get_problem_name(page):
    title = page["properties"]["Problem"]["title"]
    if not title:
        return None
    return title[0]["plain_text"]

def get_topics(page):
    topics = page["properties"]["Topic"]["multi_select"]
    return [topic["name"] for topic in topics]

def get_difficulty(page):
    difficulty = page["properties"]["Difficulty"]["select"]
    if not difficulty:
        return None
    return difficulty["name"]

def get_status(page):
    status = page["properties"]["Status"]["select"]
    if not status:
        return None
    return status["name"]

def get_confidence(page):
    return page["properties"]["Confidence"]["number"]

# ---------------- WEAK TOPICS ----------------

def get_weak_topics(pages):
    weak_topic_counts = Counter()

    for page in pages:
        confidence = get_confidence(page)

        if confidence is not None and confidence <= 2:
            for topic in get_topics(page):
                weak_topic_counts[topic] += 1

    return [topic for topic, count in weak_topic_counts.most_common()]

# ---------------- REVIEW ----------------

def get_due_reviews(pages):
    today = str(datetime.now().date())
    due = []

    for page in pages:
        name = get_problem_name(page)
        if not name:
            continue

        props = page["properties"]
        next_review = props["Next Review"]["date"]

        if next_review:
            review_date = next_review["start"][:10]

            if review_date <= today:
                due.append({
                    "name": name,
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

def get_new_problems(pages, review_names, weak_topics):
    easy, medium, hard = [], [], []

    for page in pages:
        name = get_problem_name(page)
        if not name or name in review_names:
            continue

        status = get_status(page)
        difficulty = get_difficulty(page)
        topics = get_topics(page)

        if status != "Not Started":
            continue

        if not difficulty:
            continue

        is_weak_topic = any(topic in weak_topics for topic in topics)

        item = {
            "name": name,
            "topics": topics,
            "is_weak_topic": is_weak_topic,
        }

        if difficulty == "Easy":
            easy.append(item)
        elif difficulty == "Medium":
            medium.append(item)
        elif difficulty == "Hard":
            hard.append(item)

    # Weak-topic problems come first
    easy.sort(key=lambda x: not x["is_weak_topic"])
    medium.sort(key=lambda x: not x["is_weak_topic"])
    hard.sort(key=lambda x: not x["is_weak_topic"])

    selected = []

    if easy:
        selected.append(easy[0])

    selected.extend(medium[:2])

    if hard:
        selected.append(hard[0])

    return selected

# ---------------- MAIN FLOW ----------------

pages = get_pages()

due_reviews = get_due_reviews(pages)
process_reviews(due_reviews)

pages = get_pages()

review = get_due_reviews(pages)[:3]
review_names = set([r["name"] for r in review])

weak_topics = get_weak_topics(pages)
new = get_new_problems(pages, review_names, weak_topics)

# ---------------- OUTPUT ----------------

print("\n==============================")
print("TODAY'S LEETCODE PLAN")
print("==============================")

print("\nWeak Topics:")
if weak_topics:
    for topic in weak_topics:
        print("-", topic)
else:
    print("None")

print("\n🔁 Review (max 3):")
if review:
    for problem in review:
        print("-", problem["name"])
else:
    print("None 🎉")

print("\n🆕 New (weak topics prioritized):")
if new:
    for problem in new:
        marker = "🔥" if problem["is_weak_topic"] else ""
        topic_text = ", ".join(problem["topics"])
        print(f"- {problem['name']} {marker} ({topic_text})")
else:
    print("None")

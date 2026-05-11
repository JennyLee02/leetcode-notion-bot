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

# ---------------- CURRICULUM ROTATION ----------------

CURRICULUM = [
    "Arrays & Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Heap / Priority Queue",
    "Backtracking",
    "Graphs",
    "1-D Dynamic Programming",
    "2-D Dynamic Programming",
    "Greedy",
    "Intervals",
    "Math & Geometry",
    "Bit Manipulation",
]

def get_today_focus_topic():
    day_index = datetime.now().toordinal() % len(CURRICULUM)
    return CURRICULUM[day_index]

# ---------------- NORMALIZATION ----------------

def normalize_topic(topic):
    mapping = {
        "Array": "Arrays & Hashing",
        "Arrays": "Arrays & Hashing",
        "Hashing": "Arrays & Hashing",
        "Heap": "Heap / Priority Queue",
        "Priority Queue": "Heap / Priority Queue",
        "DP": "1-D Dynamic Programming",
        "Dynamic Programming": "1-D Dynamic Programming",
    }
    return mapping.get(topic, topic)

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
            "Next Review": {"date": {"start": next_date}}
        }
    }

    requests.patch(url, headers=headers, json=payload)

# ---------------- HELPERS ----------------

def get_name(page):
    title = page["properties"]["Problem"]["title"]
    return title[0]["plain_text"] if title else None

def get_topics(page):
    topics = page["properties"]["Topic"]["multi_select"]
    return [normalize_topic(t["name"]) for t in topics]

def get_difficulty(page):
    d = page["properties"]["Difficulty"]["select"]
    return d["name"] if d else None

def get_status(page):
    s = page["properties"]["Status"]["select"]
    return s["name"] if s else None

def get_confidence(page):
    return page["properties"]["Confidence"]["number"]

# ---------------- WEAK TOPICS ----------------

def get_weak_topics(pages):
    counter = Counter()

    for page in pages:
        conf = get_confidence(page)
        if conf is not None and conf <= 2:
            for topic in get_topics(page):
                counter[topic] += 1

    return [t for t, _ in counter.most_common()]

# ---------------- REVIEW ----------------

def get_due_reviews(pages):
    today = str(datetime.now().date())
    due = []

    for page in pages:
        name = get_name(page)
        if not name:
            continue

        next_review = page["properties"]["Next Review"]["date"]

        if next_review:
            review_date = next_review["start"][:10]
            if review_date <= today:
                due.append({
                    "name": name,
                    "page_id": page["id"],
                    "props": page["properties"]
                })

    return due

def process_reviews(due):
    for item in due:
        conf = item["props"]["Confidence"]["number"]
        if conf is None:
            continue

        if conf <= 2:
            update_next_review(item["page_id"], 1)
        elif conf == 3:
            update_next_review(item["page_id"], 2)
        elif conf == 4:
            update_next_review(item["page_id"], 5)
        else:
            update_next_review(item["page_id"], 7)

# ---------------- NEW SELECTION ----------------

def score_problem(item, focus_topic, weak_topics):
    score = 0

    if focus_topic in item["topics"]:
        score += 3

    if any(topic in weak_topics for topic in item["topics"]):
        score += 2

    return score

def get_new_problems(pages, review_names, weak_topics, focus_topic):
    easy, medium, hard = [], [], []

    for page in pages:
        name = get_name(page)
        if not name or name in review_names:
            continue

        if get_status(page) != "Not Started":
            continue

        difficulty = get_difficulty(page)
        topics = get_topics(page)

        item = {
            "name": name,
            "topics": topics,
            "score": 0,
        }

        item["score"] = score_problem(item, focus_topic, weak_topics)

        if difficulty == "Easy":
            easy.append(item)
        elif difficulty == "Medium":
            medium.append(item)
        elif difficulty == "Hard":
            hard.append(item)

    easy.sort(key=lambda x: x["score"], reverse=True)
    medium.sort(key=lambda x: x["score"], reverse=True)
    hard.sort(key=lambda x: x["score"], reverse=True)

    selected = []

    if easy:
        selected.append(easy[0])

    selected.extend(medium[:2])

    if hard:
        selected.append(hard[0])

    return selected

# ---------------- MAIN ----------------

pages = get_pages()

due = get_due_reviews(pages)
process_reviews(due)

pages = get_pages()

review = get_due_reviews(pages)[:3]
review_names = set([r["name"] for r in review])

weak_topics = get_weak_topics(pages)
focus_topic = get_today_focus_topic()

new = get_new_problems(
    pages=pages,
    review_names=review_names,
    weak_topics=weak_topics,
    focus_topic=focus_topic,
)

# ---------------- OUTPUT ----------------

print("\n==============================")
print("TODAY'S LEETCODE PLAN")
print("==============================")

print(f"\n📚 Today's Focus Topic: {focus_topic}")

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

print("\n🆕 New (1 Easy, 2 Medium, 0-1 Hard):")
if new:
    for problem in new:
        marker = ""
        if focus_topic in problem["topics"]:
            marker += "📚"
        if any(topic in weak_topics for topic in problem["topics"]):
            marker += "🔥"

        print(f"- {problem['name']} {marker} ({', '.join(problem['topics'])})")
else:
    print("None")

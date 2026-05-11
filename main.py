import os
import requests
from datetime import datetime, timedelta
from collections import Counter

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ---------------- CURRICULUM ----------------

CURRICULUM = [
    "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack",
    "Binary Search", "Linked List", "Trees", "Heap / Priority Queue",
    "Backtracking", "Graphs", "1-D Dynamic Programming",
    "2-D Dynamic Programming", "Greedy", "Intervals",
    "Math & Geometry", "Bit Manipulation",
]

def get_today_focus_topic():
    return CURRICULUM[datetime.now().toordinal() % len(CURRICULUM)]

# ---------------- HELPERS ----------------

def get_name(page):
    t = page["properties"]["Problem"]["title"]
    return t[0]["plain_text"] if t else None

def get_topics(page):
    return [t["name"] for t in page["properties"]["Topic"]["multi_select"]]

def get_difficulty(page):
    d = page["properties"]["Difficulty"]["select"]
    return d["name"] if d else None

def get_status(page):
    s = page["properties"]["Status"]["select"]
    return s["name"] if s else None

def get_confidence(page):
    return page["properties"]["Confidence"]["number"]

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
            if next_review["start"][:10] <= today:
                due.append({
                    "name": name,
                    "page_id": page["id"],
                    "props": page["properties"]
                })

    return due

def update_next_review(page_id, days):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    next_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    payload = {
        "properties": {
            "Next Review": {"date": {"start": next_date}}
        }
    }

    requests.patch(url, headers=headers, json=payload)

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

# ---------------- WEAK TOPICS ----------------

def get_weak_topics(pages):
    counter = Counter()

    for page in pages:
        conf = get_confidence(page)
        if conf is not None and conf <= 2:
            for t in get_topics(page):
                counter[t] += 1

    return [t for t, _ in counter.most_common()]

# ---------------- NEW ----------------

def score(item, focus, weak):
    s = 0
    if focus in item["topics"]:
        s += 3
    if any(t in weak for t in item["topics"]):
        s += 2
    return s

def get_new(pages, review_names, weak, focus):
    easy, medium, hard = [], [], []

    for p in pages:
        name = get_name(p)
        if not name or name in review_names:
            continue

        if get_status(p) != "Not Started":
            continue

        diff = get_difficulty(p)
        topics = get_topics(p)

        item = {"name": name, "topics": topics}
        item["score"] = score(item, focus, weak)

        if diff == "Easy":
            easy.append(item)
        elif diff == "Medium":
            medium.append(item)
        elif diff == "Hard":
            hard.append(item)

    easy.sort(key=lambda x: x["score"], reverse=True)
    medium.sort(key=lambda x: x["score"], reverse=True)
    hard.sort(key=lambda x: x["score"], reverse=True)

    selected = []
    if easy: selected.append(easy[0])
    selected.extend(medium[:2])
    if hard: selected.append(hard[0])

    return selected

# ---------------- DISCORD ----------------

def send_to_discord(focus, weak, review, new):
    msg = f"🔥 **Daily LeetCode Plan**\n\n"
    msg += f"📚 Focus: {focus}\n\n"

    msg += "**Weak Topics:**\n"
    if weak:
        msg += "\n".join([f"- {t}" for t in weak]) + "\n\n"
    else:
        msg += "None\n\n"

    msg += "**Review:**\n"
    if review:
        msg += "\n".join([f"- {r['name']}" for r in review]) + "\n\n"
    else:
        msg += "None 🎉\n\n"

    msg += "**New:**\n"
    for n in new:
        msg += f"- {n['name']} ({', '.join(n['topics'])})\n"

    requests.post(DISCORD_WEBHOOK, json={"content": msg})

# ---------------- MAIN ----------------

pages = requests.post(
    f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
    headers=headers
).json()["results"]

due = get_due_reviews(pages)
process_reviews(due)

pages = requests.post(
    f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
    headers=headers
).json()["results"]

review = get_due_reviews(pages)[:3]
review_names = set([r["name"] for r in review])

weak = get_weak_topics(pages)
focus = get_today_focus_topic()

new = get_new(pages, review_names, weak, focus)

# send to discord
send_to_discord(focus, weak, review, new)

print("Sent to Discord ✅")

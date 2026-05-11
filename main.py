import os
import requests
from datetime import datetime, timedelta
from collections import Counter

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

CURRICULUM = [
    "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack",
    "Binary Search", "Linked List", "Trees", "Heap / Priority Queue",
    "Backtracking", "Graphs", "1-D Dynamic Programming",
    "2-D Dynamic Programming", "Greedy", "Intervals",
    "Math & Geometry", "Bit Manipulation",
]

def get_today_focus_topic():
    return CURRICULUM[datetime.now().toordinal() % len(CURRICULUM)]

def normalize_topic(topic):
    mapping = {
        "Array": "Arrays & Hashing",
        "Arrays": "Arrays & Hashing",
        "Hashing": "Arrays & Hashing",
        "Heap": "Heap / Priority Queue",
        "Priority Queue": "Heap / Priority Queue",
    }
    return mapping.get(topic, topic)

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    return requests.post(url, headers=headers).json()["results"]

def get_name(page):
    title = page["properties"]["Problem"]["title"]
    return title[0]["plain_text"] if title else None

def get_topics(page):
    return [normalize_topic(t["name"]) for t in page["properties"]["Topic"]["multi_select"]]

def get_difficulty(page):
    d = page["properties"]["Difficulty"]["select"]
    return d["name"] if d else None

def get_status(page):
    s = page["properties"]["Status"]["select"]
    return s["name"] if s else None

def get_confidence(page):
    return page["properties"]["Confidence"]["number"]

def update_next_review(page_id, days):
    next_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=headers,
        json={
            "properties": {
                "Next Review": {
                    "date": {"start": next_date}
                }
            }
        }
    )

def get_due_reviews(pages):
    today = str(datetime.now().date())
    due = []

    for page in pages:
        name = get_name(page)
        if not name:
            continue

        next_review = page["properties"]["Next Review"]["date"]

        if next_review and next_review["start"][:10] <= today:
            due.append({
                "name": name,
                "id": page["id"],
                "props": page["properties"],
            })

    return due

def process_reviews(due_reviews):
    for item in due_reviews:
        confidence = item["props"]["Confidence"]["number"]

        if confidence is None:
            continue

        if confidence <= 2:
            update_next_review(item["id"], 1)
        elif confidence == 3:
            update_next_review(item["id"], 2)
        elif confidence == 4:
            update_next_review(item["id"], 5)
        else:
            update_next_review(item["id"], 7)

def get_weak_topics(pages):
    counter = Counter()

    for page in pages:
        confidence = get_confidence(page)

        if confidence is not None and confidence <= 2:
            for topic in get_topics(page):
                counter[topic] += 1

    return [topic for topic, _ in counter.most_common()]

def build_problem_pool(pages, review_names):
    pool = []

    for page in pages:
        name = get_name(page)

        if not name or name in review_names:
            continue

        if get_status(page) != "Not Started":
            continue

        difficulty = get_difficulty(page)
        topics = get_topics(page)

        if not difficulty:
            continue

        pool.append({
            "name": name,
            "difficulty": difficulty,
            "topics": topics,
        })

    return pool

def pick_first(pool, difficulty, topic=None, exclude_names=None):
    exclude_names = exclude_names or set()

    for problem in pool:
        if problem["name"] in exclude_names:
            continue

        if problem["difficulty"] != difficulty:
            continue

        if topic and topic not in problem["topics"]:
            continue

        return problem

    return None

def get_balanced_new_problems(pages, review_names, weak_topics, focus_topic):
    pool = build_problem_pool(pages, review_names)
    selected = []
    selected_names = set()

    primary_weak_topic = weak_topics[0] if weak_topics else None

    def add(problem, label):
        if problem and problem["name"] not in selected_names:
            problem["label"] = label
            selected.append(problem)
            selected_names.add(problem["name"])

    # 1) Focus topic: 1 Easy + 1 Medium
    add(
        pick_first(pool, "Easy", topic=focus_topic, exclude_names=selected_names),
        "📚 Focus Easy"
    )

    add(
        pick_first(pool, "Medium", topic=focus_topic, exclude_names=selected_names),
        "📚 Focus Medium"
    )

    # 2) Weak topic: 1 Medium + 0-1 Hard
    if primary_weak_topic:
        add(
            pick_first(pool, "Medium", topic=primary_weak_topic, exclude_names=selected_names),
            "🔥 Weak Medium"
        )

        weak_hard = pick_first(pool, "Hard", topic=primary_weak_topic, exclude_names=selected_names)

        if weak_hard:
            add(weak_hard, "🔥 Weak Hard")
        else:
            add(
                pick_first(pool, "Easy", topic=primary_weak_topic, exclude_names=selected_names),
                "🔥 Weak Easy"
            )

    # 3) Fallbacks if the plan has fewer than 4 problems
    fallback_targets = [
        ("Easy", None, "Extra Easy"),
        ("Medium", focus_topic, "Extra Focus Medium"),
        ("Medium", primary_weak_topic, "Extra Weak Medium"),
        ("Hard", focus_topic, "Extra Focus Hard"),
        ("Hard", None, "Extra Hard"),
    ]

    for difficulty, topic, label in fallback_targets:
        if len(selected) >= 4:
            break

        add(
            pick_first(pool, difficulty, topic=topic, exclude_names=selected_names),
            label
        )

    return selected[:4]

def send_to_discord(focus_topic, weak_topics, review, new):
    msg = "🔥 **Daily LeetCode Plan**\n\n"
    msg += f"📚 **Focus:** {focus_topic}\n\n"

    msg += "🔥 **Weak Topics:**\n"
    if weak_topics:
        msg += "\n".join([f"- {topic}" for topic in weak_topics])
    else:
        msg += "None"
    msg += "\n\n"

    msg += "🔁 **Review (max 3):**\n"
    if review:
        msg += "\n".join([f"- {r['name']}" for r in review])
    else:
        msg += "None 🎉"
    msg += "\n\n"

    msg += "🆕 **New:**\n"
    if new:
        for problem in new:
            msg += f"- {problem['name']} — {problem['label']} ({', '.join(problem['topics'])})\n"
    else:
        msg += "None\n"

    if DISCORD_WEBHOOK:
        requests.post(DISCORD_WEBHOOK, json={"content": msg})

pages = get_pages()

due_reviews = get_due_reviews(pages)
process_reviews(due_reviews)

pages = get_pages()

review = get_due_reviews(pages)[:3]
review_names = set([r["name"] for r in review])

weak_topics = get_weak_topics(pages)
focus_topic = get_today_focus_topic()

new = get_balanced_new_problems(
    pages=pages,
    review_names=review_names,
    weak_topics=weak_topics,
    focus_topic=focus_topic,
)

send_to_discord(focus_topic, weak_topics, review, new)

print("Sent to Discord ✅")
print("Focus:", focus_topic)
print("Weak Topics:", weak_topics)
print("Review:", [r["name"] for r in review])
print("New:", [p["name"] for p in new])

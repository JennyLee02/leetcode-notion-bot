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

# ---------------- CURRICULUM ----------------

CURRICULUM = [
    "Arrays & Hashing","Two Pointers","Sliding Window","Stack",
    "Binary Search","Linked List","Trees","Heap / Priority Queue",
    "Backtracking","Graphs","1-D Dynamic Programming",
    "2-D Dynamic Programming","Greedy","Intervals",
    "Math & Geometry","Bit Manipulation",
]

def get_today_focus_topic():
    return CURRICULUM[datetime.now().toordinal() % len(CURRICULUM)]

# ---------------- NORMALIZE ----------------

def normalize(t):
    return {
        "Array":"Arrays & Hashing",
        "Hashing":"Arrays & Hashing",
        "Arrays":"Arrays & Hashing"
    }.get(t, t)

# ---------------- HELPERS ----------------

def name(p): 
    t = p["properties"]["Problem"]["title"]
    return t[0]["plain_text"] if t else None

def topics(p): 
    return [normalize(t["name"]) for t in p["properties"]["Topic"]["multi_select"]]

def diff(p):
    d = p["properties"]["Difficulty"]["select"]
    return d["name"] if d else None

def status(p):
    s = p["properties"]["Status"]["select"]
    return s["name"] if s else None

def confidence(p):
    return p["properties"]["Confidence"]["number"]

# ---------------- API ----------------

def get_pages():
    return requests.post(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
        headers=headers
    ).json()["results"]

def update_review(pid, days):
    date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    requests.patch(
        f"https://api.notion.com/v1/pages/{pid}",
        headers=headers,
        json={"properties":{"Next Review":{"date":{"start":date}}}}
    )

# ---------------- REVIEW ----------------

def due_reviews(pages):
    today = str(datetime.now().date())
    res = []

    for p in pages:
        n = name(p)
        if not n: continue

        nr = p["properties"]["Next Review"]["date"]
        if nr and nr["start"][:10] <= today:
            res.append({"name":n,"id":p["id"],"props":p["properties"]})

    return res

def process(due):
    for i in due:
        c = i["props"]["Confidence"]["number"]
        if c is None: continue

        if c <= 2: update_review(i["id"],1)
        elif c == 3: update_review(i["id"],2)
        elif c == 4: update_review(i["id"],5)
        else: update_review(i["id"],7)

# ---------------- WEAK ----------------

def weak_topics(pages):
    c = Counter()
    for p in pages:
        conf = confidence(p)
        if conf is not None and conf <= 2:
            for t in topics(p):
                c[t]+=1
    return [t for t,_ in c.most_common()]

# ---------------- NEW LOGIC ----------------

def get_new(pages, review_names, weak, focus):
    easy_w, easy_o = [], []
    med_w, med_f, med_o = [], [], []
    hard_f, hard_o = [], []

    for p in pages:
        n = name(p)
        if not n or n in review_names: continue
        if status(p) != "Not Started": continue

        t = topics(p)
        d = diff(p)

        is_weak = any(x in weak for x in t)
        is_focus = focus in t

        item = (n,t)

        if d == "Easy":
            (easy_w if is_weak else easy_o).append(item)

        elif d == "Medium":
            if is_weak: med_w.append(item)
            elif is_focus: med_f.append(item)
            else: med_o.append(item)

        elif d == "Hard":
            if is_focus: hard_f.append(item)
            else: hard_o.append(item)

    selected = []

    # Easy → MUST weak if possible
    if easy_w: selected.append(easy_w[0])
    elif easy_o: selected.append(easy_o[0])

    # Medium → weak first, then focus
    selected.extend(med_w[:2])
    if len(selected) < 3:
        selected.extend(med_f[:(3-len(selected))])
    if len(selected) < 3:
        selected.extend(med_o[:(3-len(selected))])

    # Hard → focus preferred
    if hard_f: selected.append(hard_f[0])
    elif hard_o: selected.append(hard_o[0])

    return selected

# ---------------- DISCORD ----------------

def send(focus, weak, review, new):
    msg = f"🔥 **Daily LeetCode Plan**\n\n📚 Focus: {focus}\n\n"

    msg += "**Weak Topics:**\n"
    msg += "\n".join([f"- {t}" for t in weak]) if weak else "None"
    msg += "\n\n"

    msg += "**Review:**\n"
    msg += "\n".join([f"- {r['name']}" for r in review]) if review else "None 🎉"
    msg += "\n\n"

    msg += "**New:**\n"
    for n,t in new:
        msg += f"- {n} ({', '.join(t)})\n"

    if DISCORD_WEBHOOK:
        requests.post(DISCORD_WEBHOOK,json={"content":msg})

# ---------------- MAIN ----------------

pages = get_pages()

due = due_reviews(pages)
process(due)

pages = get_pages()

review = due_reviews(pages)[:3]
review_names = set([r["name"] for r in review])

weak = weak_topics(pages)
focus = get_today_focus_topic()

new = get_new(pages, review_names, weak, focus)

send(focus, weak, review, new)

print("Sent to Discord ✅")

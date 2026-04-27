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

PROBLEMS = [
    {"problem": "Contains Duplicate", "link": "https://leetcode.com/problems/contains-duplicate/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Valid Anagram", "link": "https://leetcode.com/problems/valid-anagram/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Two Sum", "link": "https://leetcode.com/problems/two-sum/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Group Anagrams", "link": "https://leetcode.com/problems/group-anagrams/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Top K Frequent Elements", "link": "https://leetcode.com/problems/top-k-frequent-elements/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Encode and Decode Strings", "link": "https://leetcode.com/problems/encode-and-decode-strings/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Product of Array Except Self", "link": "https://leetcode.com/problems/product-of-array-except-self/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Valid Sudoku", "link": "https://leetcode.com/problems/valid-sudoku/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Longest Consecutive Sequence", "link": "https://leetcode.com/problems/longest-consecutive-sequence/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
]

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data["results"]

def create_problem(problem):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Problem": {"title": [{"text": {"content": problem["problem"]}}]},
            "URL": {"url": problem["link"]},
            "Topic": {"multi_select": [{"name": problem["topic"]}]},
            "Difficulty": {"select": {"name": problem["difficulty"]}},
            "Status": {"select": {"name": "Not Started"}},
            "Attempts": {"number": 0},
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    print(problem["problem"], response.status_code)

    if response.status_code not in [200, 201]:
        print(response.text)

def import_missing_problems():
    pages = get_pages()
    existing = set()

    for page in pages:
        name_prop = page["properties"]["Problem"]["title"]
        if name_prop:
            existing.add(name_prop[0]["plain_text"])

    for problem in PROBLEMS:
        if problem["problem"] not in existing:
            create_problem(problem)
        else:
            print(problem["problem"], "already exists")

def get_review_problems(pages):
    today = str(datetime.now().date())
    review = []

    for page in pages:
        props = page["properties"]

        name_prop = props["Problem"]["title"]
        if not name_prop:
            continue

        name = name_prop[0]["plain_text"]
        next_review = props["Next Review"]["date"]

        if next_review:
            review_date = next_review["start"][:10]

            if review_date <= today:
                review.append(name)

    return review

import_missing_problems()

pages = get_pages()
review = get_review_problems(pages)

print("\nTODAY'S PLAN")

print("\nReview:")
for r in review:
    print("-", r)

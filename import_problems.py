
import os
import requests

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

    {"problem": "Valid Palindrome", "link": "https://leetcode.com/problems/valid-palindrome/", "topic": "Two Pointers", "difficulty": "Easy"},
    {"problem": "Two Sum II - Input Array Is Sorted", "link": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "3Sum", "link": "https://leetcode.com/problems/3sum/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "Container With Most Water", "link": "https://leetcode.com/problems/container-with-most-water/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "Trapping Rain Water", "link": "https://leetcode.com/problems/trapping-rain-water/", "topic": "Two Pointers", "difficulty": "Hard"},

    {"problem": "Best Time to Buy and Sell Stock", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "topic": "Sliding Window", "difficulty": "Easy"},
    {"problem": "Longest Substring Without Repeating Characters", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "topic": "Sliding Window", "difficulty": "Medium"},
    {"problem": "Longest Repeating Character Replacement", "link": "https://leetcode.com/problems/longest-repeating-character-replacement/", "topic": "Sliding Window", "difficulty": "Medium"},
    {"problem": "Permutation in String", "link": "https://leetcode.com/problems/permutation-in-string/", "topic": "Sliding Window", "difficulty": "Medium"},
]

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    return response.json()["results"]

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

pages = get_pages()
existing = set()

for page in pages:
    name_prop = page["properties"]["Problem"]["title"]
    if name_prop:
        existing.add(name_prop[0]["plain_text"])

for problem in PROBLEMS:
    if problem["problem"] in existing:
        print(problem["problem"], "already exists")
    else:
        create_problem(problem)

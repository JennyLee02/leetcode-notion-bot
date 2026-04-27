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
    # Arrays & Hashing
    {"problem": "Contains Duplicate", "link": "https://leetcode.com/problems/contains-duplicate/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Valid Anagram", "link": "https://leetcode.com/problems/valid-anagram/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Two Sum", "link": "https://leetcode.com/problems/two-sum/", "topic": "Arrays & Hashing", "difficulty": "Easy"},
    {"problem": "Group Anagrams", "link": "https://leetcode.com/problems/group-anagrams/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Top K Frequent Elements", "link": "https://leetcode.com/problems/top-k-frequent-elements/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Encode and Decode Strings", "link": "https://leetcode.com/problems/encode-and-decode-strings/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Product of Array Except Self", "link": "https://leetcode.com/problems/product-of-array-except-self/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Valid Sudoku", "link": "https://leetcode.com/problems/valid-sudoku/", "topic": "Arrays & Hashing", "difficulty": "Medium"},
    {"problem": "Longest Consecutive Sequence", "link": "https://leetcode.com/problems/longest-consecutive-sequence/", "topic": "Arrays & Hashing", "difficulty": "Medium"},

    # Two Pointers
    {"problem": "Valid Palindrome", "link": "https://leetcode.com/problems/valid-palindrome/", "topic": "Two Pointers", "difficulty": "Easy"},
    {"problem": "Two Sum II - Input Array Is Sorted", "link": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "3Sum", "link": "https://leetcode.com/problems/3sum/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "Container With Most Water", "link": "https://leetcode.com/problems/container-with-most-water/", "topic": "Two Pointers", "difficulty": "Medium"},
    {"problem": "Trapping Rain Water", "link": "https://leetcode.com/problems/trapping-rain-water/", "topic": "Two Pointers", "difficulty": "Hard"},

    # Sliding Window
    {"problem": "Best Time to Buy and Sell Stock", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "topic": "Sliding Window", "difficulty": "Easy"},
    {"problem": "Longest Substring Without Repeating Characters", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "topic": "Sliding Window", "difficulty": "Medium"},
    {"problem": "Longest Repeating Character Replacement", "link": "https://leetcode.com/problems/longest-repeating-character-replacement/", "topic": "Sliding Window", "difficulty": "Medium"},
    {"problem": "Permutation in String", "link": "https://leetcode.com/problems/permutation-in-string/", "topic": "Sliding Window", "difficulty": "Medium"},
    {"problem": "Minimum Window Substring", "link": "https://leetcode.com/problems/minimum-window-substring/", "topic": "Sliding Window", "difficulty": "Hard"},
    {"problem": "Sliding Window Maximum", "link": "https://leetcode.com/problems/sliding-window-maximum/", "topic": "Sliding Window", "difficulty": "Hard"},

    # Stack
    {"problem": "Valid Parentheses", "link": "https://leetcode.com/problems/valid-parentheses/", "topic": "Stack", "difficulty": "Easy"},
    {"problem": "Min Stack", "link": "https://leetcode.com/problems/min-stack/", "topic": "Stack", "difficulty": "Medium"},
    {"problem": "Evaluate Reverse Polish Notation", "link": "https://leetcode.com/problems/evaluate-reverse-polish-notation/", "topic": "Stack", "difficulty": "Medium"},
    {"problem": "Generate Parentheses", "link": "https://leetcode.com/problems/generate-parentheses/", "topic": "Stack", "difficulty": "Medium"},
    {"problem": "Daily Temperatures", "link": "https://leetcode.com/problems/daily-temperatures/", "topic": "Stack", "difficulty": "Medium"},
    {"problem": "Car Fleet", "link": "https://leetcode.com/problems/car-fleet/", "topic": "Stack", "difficulty": "Medium"},
    {"problem": "Largest Rectangle in Histogram", "link": "https://leetcode.com/problems/largest-rectangle-in-histogram/", "topic": "Stack", "difficulty": "Hard"},

    # Binary Search
    {"problem": "Binary Search", "link": "https://leetcode.com/problems/binary-search/", "topic": "Binary Search", "difficulty": "Easy"},
    {"problem": "Search a 2D Matrix", "link": "https://leetcode.com/problems/search-a-2d-matrix/", "topic": "Binary Search", "difficulty": "Medium"},
    {"problem": "Koko Eating Bananas", "link": "https://leetcode.com/problems/koko-eating-bananas/", "topic": "Binary Search", "difficulty": "Medium"},
    {"problem": "Find Minimum in Rotated Sorted Array", "link": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/", "topic": "Binary Search", "difficulty": "Medium"},
    {"problem": "Search in Rotated Sorted Array", "link": "https://leetcode.com/problems/search-in-rotated-sorted-array/", "topic": "Binary Search", "difficulty": "Medium"},
    {"problem": "Time Based Key-Value Store", "link": "https://leetcode.com/problems/time-based-key-value-store/", "topic": "Binary Search", "difficulty": "Medium"},
    {"problem": "Median of Two Sorted Arrays", "link": "https://leetcode.com/problems/median-of-two-sorted-arrays/", "topic": "Binary Search", "difficulty": "Hard"},

    # Linked List
    {"problem": "Reverse Linked List", "link": "https://leetcode.com/problems/reverse-linked-list/", "topic": "Linked List", "difficulty": "Easy"},
    {"problem": "Merge Two Sorted Lists", "link": "https://leetcode.com/problems/merge-two-sorted-lists/", "topic": "Linked List", "difficulty": "Easy"},
    {"problem": "Linked List Cycle", "link": "https://leetcode.com/problems/linked-list-cycle/", "topic": "Linked List", "difficulty": "Easy"},
    {"problem": "Reorder List", "link": "https://leetcode.com/problems/reorder-list/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "Remove Nth Node From End of List", "link": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "Copy List with Random Pointer", "link": "https://leetcode.com/problems/copy-list-with-random-pointer/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "Add Two Numbers", "link": "https://leetcode.com/problems/add-two-numbers/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "Find the Duplicate Number", "link": "https://leetcode.com/problems/find-the-duplicate-number/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "LRU Cache", "link": "https://leetcode.com/problems/lru-cache/", "topic": "Linked List", "difficulty": "Medium"},
    {"problem": "Merge K Sorted Lists", "link": "https://leetcode.com/problems/merge-k-sorted-lists/", "topic": "Linked List", "difficulty": "Hard"},
    {"problem": "Reverse Nodes in k-Group", "link": "https://leetcode.com/problems/reverse-nodes-in-k-group/", "topic": "Linked List", "difficulty": "Hard"},

    # Trees
    {"problem": "Invert Binary Tree", "link": "https://leetcode.com/problems/invert-binary-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Maximum Depth of Binary Tree", "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Diameter of Binary Tree", "link": "https://leetcode.com/problems/diameter-of-binary-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Balanced Binary Tree", "link": "https://leetcode.com/problems/balanced-binary-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Same Tree", "link": "https://leetcode.com/problems/same-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Subtree of Another Tree", "link": "https://leetcode.com/problems/subtree-of-another-tree/", "topic": "Trees", "difficulty": "Easy"},
    {"problem": "Lowest Common Ancestor of a Binary Search Tree", "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Binary Tree Level Order Traversal", "link": "https://leetcode.com/problems/binary-tree-level-order-traversal/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Binary Tree Right Side View", "link": "https://leetcode.com/problems/binary-tree-right-side-view/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Count Good Nodes in Binary Tree", "link": "https://leetcode.com/problems/count-good-nodes-in-binary-tree/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Validate Binary Search Tree", "link": "https://leetcode.com/problems/validate-binary-search-tree/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Kth Smallest Element in a BST", "link": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Construct Binary Tree from Preorder and Inorder Traversal", "link": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/", "topic": "Trees", "difficulty": "Medium"},
    {"problem": "Binary Tree Maximum Path Sum", "link": "https://leetcode.com/problems/binary-tree-maximum-path-sum/", "topic": "Trees", "difficulty": "Hard"},
    {"problem": "Serialize and Deserialize Binary Tree", "link": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/", "topic": "Trees", "difficulty": "Hard"},

    # Tries
    {"problem": "Implement Trie Prefix Tree", "link": "https://leetcode.com/problems/implement-trie-prefix-tree/", "topic": "Tries", "difficulty": "Medium"},
    {"problem": "Design Add and Search Words Data Structure", "link": "https://leetcode.com/problems/design-add-and-search-words-data-structure/", "topic": "Tries", "difficulty": "Medium"},
    {"problem": "Word Search II", "link": "https://leetcode.com/problems/word-search-ii/", "topic": "Tries", "difficulty": "Hard"},

    # Heap / Priority Queue
    {"problem": "Kth Largest Element in a Stream", "link": "https://leetcode.com/problems/kth-largest-element-in-a-stream/", "topic": "Heap / Priority Queue", "difficulty": "Easy"},
    {"problem": "Last Stone Weight", "link": "https://leetcode.com/problems/last-stone-weight/", "topic": "Heap / Priority Queue", "difficulty": "Easy"},
    {"problem": "K Closest Points to Origin", "link": "https://leetcode.com/problems/k-closest-points-to-origin/", "topic": "Heap / Priority Queue", "difficulty": "Medium"},
    {"problem": "Kth Largest Element in an Array", "link": "https://leetcode.com/problems/kth-largest-element-in-an-array/", "topic": "Heap / Priority Queue", "difficulty": "Medium"},
    {"problem": "Task Scheduler", "link": "https://leetcode.com/problems/task-scheduler/", "topic": "Heap / Priority Queue", "difficulty": "Medium"},
    {"problem": "Design Twitter", "link": "https://leetcode.com/problems/design-twitter/", "topic": "Heap / Priority Queue", "difficulty": "Medium"},
    {"problem": "Find Median from Data Stream", "link": "https://leetcode.com/problems/find-median-from-data-stream/", "topic": "Heap / Priority Queue", "difficulty": "Hard"},

        # Backtracking
    {"problem": "Subsets", "link": "https://leetcode.com/problems/subsets/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Combination Sum", "link": "https://leetcode.com/problems/combination-sum/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Permutations", "link": "https://leetcode.com/problems/permutations/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Subsets II", "link": "https://leetcode.com/problems/subsets-ii/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Combination Sum II", "link": "https://leetcode.com/problems/combination-sum-ii/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Word Search", "link": "https://leetcode.com/problems/word-search/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Palindrome Partitioning", "link": "https://leetcode.com/problems/palindrome-partitioning/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "Letter Combinations of a Phone Number", "link": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/", "topic": "Backtracking", "difficulty": "Medium"},
    {"problem": "N-Queens", "link": "https://leetcode.com/problems/n-queens/", "topic": "Backtracking", "difficulty": "Hard"},

    # Graphs
    {"problem": "Number of Islands", "link": "https://leetcode.com/problems/number-of-islands/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Clone Graph", "link": "https://leetcode.com/problems/clone-graph/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Max Area of Island", "link": "https://leetcode.com/problems/max-area-of-island/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Pacific Atlantic Water Flow", "link": "https://leetcode.com/problems/pacific-atlantic-water-flow/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Surrounded Regions", "link": "https://leetcode.com/problems/surrounded-regions/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Rotting Oranges", "link": "https://leetcode.com/problems/rotting-oranges/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Walls and Gates", "link": "https://leetcode.com/problems/walls-and-gates/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Course Schedule", "link": "https://leetcode.com/problems/course-schedule/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Course Schedule II", "link": "https://leetcode.com/problems/course-schedule-ii/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Redundant Connection", "link": "https://leetcode.com/problems/redundant-connection/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Number of Connected Components in an Undirected Graph", "link": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Graph Valid Tree", "link": "https://leetcode.com/problems/graph-valid-tree/", "topic": "Graphs", "difficulty": "Medium"},
    {"problem": "Word Ladder", "link": "https://leetcode.com/problems/word-ladder/", "topic": "Graphs", "difficulty": "Hard"},

    # Advanced Graphs
    {"problem": "Reconstruct Itinerary", "link": "https://leetcode.com/problems/reconstruct-itinerary/", "topic": "Advanced Graphs", "difficulty": "Hard"},
    {"problem": "Min Cost to Connect All Points", "link": "https://leetcode.com/problems/min-cost-to-connect-all-points/", "topic": "Advanced Graphs", "difficulty": "Medium"},
    {"problem": "Network Delay Time", "link": "https://leetcode.com/problems/network-delay-time/", "topic": "Advanced Graphs", "difficulty": "Medium"},
    {"problem": "Swim in Rising Water", "link": "https://leetcode.com/problems/swim-in-rising-water/", "topic": "Advanced Graphs", "difficulty": "Hard"},
    {"problem": "Alien Dictionary", "link": "https://leetcode.com/problems/alien-dictionary/", "topic": "Advanced Graphs", "difficulty": "Hard"},
    {"problem": "Cheapest Flights Within K Stops", "link": "https://leetcode.com/problems/cheapest-flights-within-k-stops/", "topic": "Advanced Graphs", "difficulty": "Medium"},

    # 1-D Dynamic Programming
    {"problem": "Climbing Stairs", "link": "https://leetcode.com/problems/climbing-stairs/", "topic": "1-D Dynamic Programming", "difficulty": "Easy"},
    {"problem": "Min Cost Climbing Stairs", "link": "https://leetcode.com/problems/min-cost-climbing-stairs/", "topic": "1-D Dynamic Programming", "difficulty": "Easy"},
    {"problem": "House Robber", "link": "https://leetcode.com/problems/house-robber/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "House Robber II", "link": "https://leetcode.com/problems/house-robber-ii/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Longest Palindromic Substring", "link": "https://leetcode.com/problems/longest-palindromic-substring/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Palindromic Substrings", "link": "https://leetcode.com/problems/palindromic-substrings/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Decode Ways", "link": "https://leetcode.com/problems/decode-ways/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Coin Change", "link": "https://leetcode.com/problems/coin-change/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Maximum Product Subarray", "link": "https://leetcode.com/problems/maximum-product-subarray/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Word Break", "link": "https://leetcode.com/problems/word-break/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Longest Increasing Subsequence", "link": "https://leetcode.com/problems/longest-increasing-subsequence/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Partition Equal Subset Sum", "link": "https://leetcode.com/problems/partition-equal-subset-sum/", "topic": "1-D Dynamic Programming", "difficulty": "Medium"},

    # 2-D Dynamic Programming
    {"problem": "Unique Paths", "link": "https://leetcode.com/problems/unique-paths/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Longest Common Subsequence", "link": "https://leetcode.com/problems/longest-common-subsequence/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Best Time to Buy and Sell Stock with Cooldown", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Coin Change II", "link": "https://leetcode.com/problems/coin-change-ii/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Target Sum", "link": "https://leetcode.com/problems/target-sum/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Interleaving String", "link": "https://leetcode.com/problems/interleaving-string/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Longest Increasing Path in a Matrix", "link": "https://leetcode.com/problems/longest-increasing-path-in-a-matrix/", "topic": "2-D Dynamic Programming", "difficulty": "Hard"},
    {"problem": "Distinct Subsequences", "link": "https://leetcode.com/problems/distinct-subsequences/", "topic": "2-D Dynamic Programming", "difficulty": "Hard"},
    {"problem": "Edit Distance", "link": "https://leetcode.com/problems/edit-distance/", "topic": "2-D Dynamic Programming", "difficulty": "Medium"},
    {"problem": "Burst Balloons", "link": "https://leetcode.com/problems/burst-balloons/", "topic": "2-D Dynamic Programming", "difficulty": "Hard"},
    {"problem": "Regular Expression Matching", "link": "https://leetcode.com/problems/regular-expression-matching/", "topic": "2-D Dynamic Programming", "difficulty": "Hard"},

    # Greedy
    {"problem": "Maximum Subarray", "link": "https://leetcode.com/problems/maximum-subarray/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Jump Game", "link": "https://leetcode.com/problems/jump-game/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Jump Game II", "link": "https://leetcode.com/problems/jump-game-ii/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Gas Station", "link": "https://leetcode.com/problems/gas-station/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Hand of Straights", "link": "https://leetcode.com/problems/hand-of-straights/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Merge Triplets to Form Target Triplet", "link": "https://leetcode.com/problems/merge-triplets-to-form-target-triplet/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Partition Labels", "link": "https://leetcode.com/problems/partition-labels/", "topic": "Greedy", "difficulty": "Medium"},
    {"problem": "Valid Parenthesis String", "link": "https://leetcode.com/problems/valid-parenthesis-string/", "topic": "Greedy", "difficulty": "Medium"},

    # Intervals
    {"problem": "Insert Interval", "link": "https://leetcode.com/problems/insert-interval/", "topic": "Intervals", "difficulty": "Medium"},
    {"problem": "Merge Intervals", "link": "https://leetcode.com/problems/merge-intervals/", "topic": "Intervals", "difficulty": "Medium"},
    {"problem": "Non-overlapping Intervals", "link": "https://leetcode.com/problems/non-overlapping-intervals/", "topic": "Intervals", "difficulty": "Medium"},
    {"problem": "Meeting Rooms", "link": "https://leetcode.com/problems/meeting-rooms/", "topic": "Intervals", "difficulty": "Easy"},
    {"problem": "Meeting Rooms II", "link": "https://leetcode.com/problems/meeting-rooms-ii/", "topic": "Intervals", "difficulty": "Medium"},
    {"problem": "Minimum Interval to Include Each Query", "link": "https://leetcode.com/problems/minimum-interval-to-include-each-query/", "topic": "Intervals", "difficulty": "Hard"},

    # Math & Geometry
    {"problem": "Rotate Image", "link": "https://leetcode.com/problems/rotate-image/", "topic": "Math & Geometry", "difficulty": "Medium"},
    {"problem": "Spiral Matrix", "link": "https://leetcode.com/problems/spiral-matrix/", "topic": "Math & Geometry", "difficulty": "Medium"},
    {"problem": "Set Matrix Zeroes", "link": "https://leetcode.com/problems/set-matrix-zeroes/", "topic": "Math & Geometry", "difficulty": "Medium"},
    {"problem": "Happy Number", "link": "https://leetcode.com/problems/happy-number/", "topic": "Math & Geometry", "difficulty": "Easy"},
    {"problem": "Plus One", "link": "https://leetcode.com/problems/plus-one/", "topic": "Math & Geometry", "difficulty": "Easy"},
    {"problem": "Pow(x, n)", "link": "https://leetcode.com/problems/powx-n/", "topic": "Math & Geometry", "difficulty": "Medium"},
    {"problem": "Multiply Strings", "link": "https://leetcode.com/problems/multiply-strings/", "topic": "Math & Geometry", "difficulty": "Medium"},
    {"problem": "Detect Squares", "link": "https://leetcode.com/problems/detect-squares/", "topic": "Math & Geometry", "difficulty": "Medium"},

    # Bit Manipulation
    {"problem": "Single Number", "link": "https://leetcode.com/problems/single-number/", "topic": "Bit Manipulation", "difficulty": "Easy"},
    {"problem": "Number of 1 Bits", "link": "https://leetcode.com/problems/number-of-1-bits/", "topic": "Bit Manipulation", "difficulty": "Easy"},
    {"problem": "Counting Bits", "link": "https://leetcode.com/problems/counting-bits/", "topic": "Bit Manipulation", "difficulty": "Easy"},
    {"problem": "Reverse Bits", "link": "https://leetcode.com/problems/reverse-bits/", "topic": "Bit Manipulation", "difficulty": "Easy"},
    {"problem": "Missing Number", "link": "https://leetcode.com/problems/missing-number/", "topic": "Bit Manipulation", "difficulty": "Easy"},
    {"problem": "Sum of Two Integers", "link": "https://leetcode.com/problems/sum-of-two-integers/", "topic": "Bit Manipulation", "difficulty": "Medium"},
    {"problem": "Reverse Integer", "link": "https://leetcode.com/problems/reverse-integer/", "topic": "Bit Manipulation", "difficulty": "Medium"},
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

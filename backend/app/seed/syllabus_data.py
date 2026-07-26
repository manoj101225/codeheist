"""
Full seed data for CodeHeist — 14 districts, 150+ missions, all with GTA-themed heist names.
Each mission includes: description, starter code for all 4 languages, test cases.
"""

DISTRICTS = [
    {
        "name": "Downtown Turf War",
        "slug": "downtown-turf-war",
        "description": "The concrete jungle where every street corner is contested. Master array operations to control the crew lineup and dominate downtown.",
        "topic": "Arrays",
        "order": 1,
        "color": "#ff0040",
        "icon": "🏙️",
        "x": 400, "y": 300,
        "unlock_requirement": 0,
    },
    {
        "name": "The Sniper's Perch",
        "slug": "snipers-perch",
        "description": "From the rooftops, precision is everything. Binary search is your scope — find any target in the sorted city below.",
        "topic": "Binary Search",
        "order": 2,
        "color": "#00ff88",
        "icon": "🔭",
        "x": 650, "y": 200,
        "unlock_requirement": 5,
    },
    {
        "name": "The Wiretap Room",
        "slug": "wiretap-room",
        "description": "Every conversation is recorded. Decode strings, intercept messages, and crack encrypted communications.",
        "topic": "Strings",
        "order": 3,
        "color": "#00ccff",
        "icon": "🎧",
        "x": 250, "y": 150,
        "unlock_requirement": 5,
    },
    {
        "name": "The Chain of Command",
        "slug": "chain-of-command",
        "description": "The hierarchy runs deep. Navigate linked lists to control the chain of command from boss to foot soldier.",
        "topic": "Linked Lists",
        "order": 4,
        "color": "#ff8800",
        "icon": "🔗",
        "x": 550, "y": 450,
        "unlock_requirement": 5,
    },
    {
        "name": "The Maze Heist",
        "slug": "maze-heist",
        "description": "Every heist has multiple paths. Use recursion and backtracking to explore every possible escape route.",
        "topic": "Recursion & Backtracking",
        "order": 5,
        "color": "#cc00ff",
        "icon": "🌀",
        "x": 150, "y": 400,
        "unlock_requirement": 5,
    },
    {
        "name": "The Signal Jammer",
        "slug": "signal-jammer",
        "description": "Jam the frequencies. Bit manipulation lets you control signals at the lowest level — flip, mask, and shift your way to dominance.",
        "topic": "Bit Manipulation",
        "order": 6,
        "color": "#ffff00",
        "icon": "📡",
        "x": 700, "y": 350,
        "unlock_requirement": 5,
    },
    {
        "name": "The Escape Route",
        "slug": "escape-route",
        "description": "When the heat is on, you need stacks and queues. Manage your escape routes with precision — LIFO for emergencies, FIFO for planning.",
        "topic": "Stack & Queue",
        "order": 7,
        "color": "#ff4488",
        "icon": "🚪",
        "x": 350, "y": 500,
        "unlock_requirement": 5,
    },
    {
        "name": "The Stakeout",
        "slug": "stakeout",
        "description": "Patience and observation. The sliding window technique lets you survey any stretch of territory without missing a beat.",
        "topic": "Sliding Window",
        "order": 8,
        "color": "#88ff00",
        "icon": "🔍",
        "x": 500, "y": 100,
        "unlock_requirement": 5,
    },
    {
        "name": "The Most Wanted Board",
        "slug": "most-wanted-board",
        "description": "The priority list of the underworld. Heaps keep the most dangerous targets at the top — always ready for action.",
        "topic": "Heaps",
        "order": 9,
        "color": "#ff6600",
        "icon": "📋",
        "x": 200, "y": 280,
        "unlock_requirement": 5,
    },
    {
        "name": "The Negotiation Table",
        "slug": "negotiation-table",
        "description": "In the underworld, greed is a strategy. Make the optimal choice at every step — no looking back.",
        "topic": "Greedy",
        "order": 10,
        "color": "#00ffcc",
        "icon": "🤝",
        "x": 600, "y": 380,
        "unlock_requirement": 5,
    },
    {
        "name": "The Family Tree",
        "slug": "family-tree",
        "description": "Every crime family has a hierarchy. Traverse the binary tree to understand who answers to whom.",
        "topic": "Binary Trees",
        "order": 11,
        "color": "#ff0088",
        "icon": "🌳",
        "x": 450, "y": 200,
        "unlock_requirement": 5,
    },
    {
        "name": "The Ledger",
        "slug": "ledger",
        "description": "The books must be balanced. Binary search trees keep the crime records organized and searchable.",
        "topic": "BST",
        "order": 12,
        "color": "#8800ff",
        "icon": "📒",
        "x": 300, "y": 350,
        "unlock_requirement": 5,
    },
    {
        "name": "The City Map",
        "slug": "city-map",
        "description": "The entire city is a graph — every intersection a node, every road an edge. Master graph algorithms to control all routes.",
        "topic": "Graphs",
        "order": 13,
        "color": "#0088ff",
        "icon": "🗺️",
        "x": 500, "y": 300,
        "unlock_requirement": 5,
    },
    {
        "name": "The Vault",
        "slug": "vault",
        "description": "The final heist. Dynamic programming is the master key — break down the impossible into solved subproblems and crack the vault.",
        "topic": "Dynamic Programming",
        "order": 14,
        "color": "#ffd700",
        "icon": "🏦",
        "x": 400, "y": 450,
        "unlock_requirement": 5,
    },
]


# ─────────────────────── MISSIONS ───────────────────────
# Each mission: title, subtitle (real problem), description, difficulty, starter code, test cases

MISSIONS = {
    "downtown-turf-war": [
        {
            "title": "The Crew Lineup",
            "subtitle": "Find Largest Element in Array",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## The Crew Lineup

The boss needs to know who the strongest fighter in the crew is. Given an array of crew members' power levels, find the maximum power level.

### Input
- First line: integer N (size of the array)
- Second line: N space-separated integers (power levels)

### Output
- A single integer: the maximum power level

### Example
```
Input:
5
3 7 2 9 1

Output:
9
```

### Constraints
- 1 ≤ N ≤ 10^5
- -10^9 ≤ arr[i] ≤ 10^9""",
            "starter_python": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int findMax(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int findMax(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar findMax = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Iterate through the array keeping track of the maximum value seen so far.",
            "hint_2": "Initialize max with the first element or negative infinity.",
            "test_cases": [
                {"input": "5\n3 7 2 9 1", "expected": "9", "is_hidden": False},
                {"input": "3\n-1 -5 -3", "expected": "-1", "is_hidden": False},
                {"input": "1\n42", "expected": "42", "is_hidden": True},
                {"input": "6\n1 1 1 1 1 1", "expected": "1", "is_hidden": True},
            ],
        },
        {
            "title": "Second-in-Command",
            "subtitle": "Second Largest Element",
            "difficulty": "Easy",
            "order": 2,
            "reputation_reward": 100,
            "description": """## Second-in-Command

Every boss has a second-in-command. Find the second largest element in the crew's power lineup. If no second largest exists, print -1.

### Input
- First line: integer N
- Second line: N space-separated integers

### Output
- The second largest element, or -1 if it doesn't exist

### Example
```
Input:
5
3 7 2 9 1

Output:
7
```""",
            "starter_python": "class Solution:\n    def secondLargest(self, nums: list[int]) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int secondLargest(vector<int>& nums) {\n        // Write your solution here\n        return -1;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int secondLargest(int[] nums) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar secondLargest = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Track both the largest and second largest in a single pass.",
            "hint_2": "When you find a new largest, the old largest becomes the second largest.",
            "test_cases": [
                {"input": "5\n3 7 2 9 1", "expected": "7", "is_hidden": False},
                {"input": "3\n5 5 5", "expected": "-1", "is_hidden": False},
                {"input": "2\n1 2", "expected": "1", "is_hidden": True},
                {"input": "4\n10 10 9 8", "expected": "9", "is_hidden": True},
            ],
        },
        {
            "title": "Two-Man Job",
            "subtitle": "Two Sum",
            "difficulty": "Easy",
            "order": 3,
            "reputation_reward": 100,
            "description": """## Two-Man Job

The boss needs exactly two crew members whose combined power equals a target value for a heist. Find the indices (0-based) of the two members. Guaranteed exactly one solution exists.

### Input
- First line: integers N and TARGET
- Second line: N space-separated integers

### Output
- Two space-separated indices

### Example
```
Input:
4 9
2 7 11 15

Output:
0 1
```""",
            "starter_python": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number[]}\n */\nvar twoSum = function(nums, target) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use a hash map to store each number and its index as you iterate.",
            "hint_2": "For each element, check if (target - element) exists in the map.",
            "test_cases": [
                {"input": "4 9\n2 7 11 15", "expected": "0 1", "is_hidden": False},
                {"input": "3 6\n3 2 4", "expected": "1 2", "is_hidden": False},
                {"input": "2 6\n3 3", "expected": "0 1", "is_hidden": True},
            ],
        },
        {
            "title": "Zero Witness Protection",
            "subtitle": "Move Zeros to End",
            "difficulty": "Easy",
            "order": 4,
            "reputation_reward": 100,
            "description": """## Zero Witness Protection

The snitches (zeros) need to be moved to the end of the lineup. Move all zeros to the end while maintaining the relative order of non-zero elements.

### Input
- First line: integer N
- Second line: N space-separated integers

### Output
- The modified array, space-separated

### Example
```
Input:
5
0 1 0 3 12

Output:
1 3 12 0 0
```""",
            "starter_python": "class Solution:\n    def moveZeroes(self, nums: list[int]) -> list[int]:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> moveZeroes(vector<int>& nums) {\n        // Write your solution here\n        return nums;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int[] moveZeroes(int[] nums) {\n        // Write your solution here\n        return nums;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number[]}\n */\nvar moveZeroes = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use two pointers — one for the current position and one for placing non-zero elements.",
            "hint_2": "Swap non-zero elements to the front, then fill remaining positions with zeros.",
            "test_cases": [
                {"input": "5\n0 1 0 3 12", "expected": "1 3 12 0 0", "is_hidden": False},
                {"input": "1\n0", "expected": "0", "is_hidden": False},
                {"input": "4\n1 2 3 4", "expected": "1 2 3 4", "is_hidden": True},
                {"input": "3\n0 0 1", "expected": "1 0 0", "is_hidden": True},
            ],
        },
        {
            "title": "The Longest Winning Streak",
            "subtitle": "Kadane's Maximum Subarray",
            "difficulty": "Medium",
            "order": 5,
            "reputation_reward": 250,
            "description": """## The Longest Winning Streak

The crew has been running heists with varying profits and losses. Find the maximum sum of any contiguous subarray — the longest winning streak of profit.

### Input
- First line: integer N
- Second line: N space-separated integers (can be negative)

### Output
- The maximum subarray sum

### Example
```
Input:
9
-2 1 -3 4 -1 2 1 -5 4

Output:
6
```

Explanation: [4, -1, 2, 1] has the largest sum = 6.""",
            "starter_python": "class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int maxSubArray(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar maxSubArray = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Kadane's Algorithm: keep a running sum, reset to 0 when it goes negative.",
            "hint_2": "Track the maximum sum seen so far. The answer is this global maximum.",
            "test_cases": [
                {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected": "6", "is_hidden": False},
                {"input": "1\n-1", "expected": "-1", "is_hidden": False},
                {"input": "5\n1 2 3 4 5", "expected": "15", "is_hidden": True},
                {"input": "3\n-2 -3 -1", "expected": "-1", "is_hidden": True},
            ],
        },
        {
            "title": "Majority Boss Vote",
            "subtitle": "Majority Element (> n/2)",
            "difficulty": "Medium",
            "order": 6,
            "reputation_reward": 250,
            "description": """## Majority Boss Vote

The crew is voting for the new boss. Find the element that appears more than n/2 times. It is guaranteed that such an element exists.

### Input
- First line: integer N
- Second line: N space-separated integers

### Output
- The majority element

### Example
```
Input:
7
2 2 1 1 1 2 2

Output:
2
```""",
            "starter_python": "class Solution:\n    def majorityElement(self, nums: list[int]) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int majorityElement(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int majorityElement(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar majorityElement = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Boyer-Moore Voting Algorithm: maintain a candidate and a count.",
            "hint_2": "Increment count if same as candidate, decrement otherwise. When count = 0, pick new candidate.",
            "test_cases": [
                {"input": "7\n2 2 1 1 1 2 2", "expected": "2", "is_hidden": False},
                {"input": "3\n3 2 3", "expected": "3", "is_hidden": False},
                {"input": "1\n1", "expected": "1", "is_hidden": True},
            ],
        },
        {
            "title": "Rotate the Getaway Van",
            "subtitle": "Rotate Array by K",
            "difficulty": "Medium",
            "order": 7,
            "reputation_reward": 250,
            "description": """## Rotate the Getaway Van

Rotate the crew lineup to the right by K positions. The last K members move to the front.

### Input
- First line: integers N and K
- Second line: N space-separated integers

### Output
- The rotated array, space-separated

### Example
```
Input:
7 3
1 2 3 4 5 6 7

Output:
5 6 7 1 2 3 4
```""",
            "starter_python": "class Solution:\n    def rotate(self, nums: list[int], k: int) -> list[int]:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> rotate(vector<int>& nums, int k) {\n        // Write your solution here\n        return nums;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int[] rotate(int[] nums, int k) {\n        // Write your solution here\n        return nums;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @param {number} k\n * @return {number[]}\n */\nvar rotate = function(nums, k) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use the reverse trick: reverse entire array, then reverse first k, then reverse remaining.",
            "hint_2": "Don't forget to handle k > n by taking k = k % n.",
            "test_cases": [
                {"input": "7 3\n1 2 3 4 5 6 7", "expected": "5 6 7 1 2 3 4", "is_hidden": False},
                {"input": "3 1\n1 2 3", "expected": "3 1 2", "is_hidden": False},
                {"input": "4 4\n1 2 3 4", "expected": "1 2 3 4", "is_hidden": True},
                {"input": "5 7\n1 2 3 4 5", "expected": "4 5 1 2 3", "is_hidden": True},
            ],
        },
        {
            "title": "Snitch Removal",
            "subtitle": "Remove Duplicates from Sorted Array",
            "difficulty": "Easy",
            "order": 8,
            "reputation_reward": 100,
            "description": """## Snitch Removal

Clean the sorted crew roster — remove duplicate entries and print the unique members count followed by the cleaned array.

### Input
- First line: integer N
- Second line: N sorted space-separated integers

### Output
- First line: count of unique elements
- Second line: unique elements, space-separated

### Example
```
Input:
7
1 1 2 2 3 3 3

Output:
3
1 2 3
```""",
            "starter_python": "class Solution:\n    def removeDuplicates(self, nums: list[int]) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int removeDuplicates(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int removeDuplicates(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number}\n */\nvar removeDuplicates = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use two pointers — one slow, one fast.",
            "hint_2": "When fast pointer finds a new element, place it at slow+1 position.",
            "test_cases": [
                {"input": "7\n1 1 2 2 3 3 3", "expected": "3\n1 2 3", "is_hidden": False},
                {"input": "1\n5", "expected": "1\n5", "is_hidden": False},
                {"input": "5\n1 2 3 4 5", "expected": "5\n1 2 3 4 5", "is_hidden": True},
            ],
        },
    ],
    "snipers-perch": [
        {
            "title": "Target Acquired",
            "subtitle": "Classic Binary Search",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## Target Acquired

Your sniper scope has a sorted list of targets. Find the exact position of a given target using binary search. Print the 0-based index, or -1 if not found.

### Input
- First line: integers N and TARGET
- Second line: N sorted space-separated integers

### Output
- Index of target, or -1

### Example
```
Input:
5 7
1 3 5 7 9

Output:
3
```""",
            "starter_python": "class Solution:\n    def search(self, nums: list[int], target: int) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number}\n */\nvar search = function(nums, target) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use two pointers low and high. Check mid = (low + high) / 2.",
            "hint_2": "If arr[mid] < target, search right half. If arr[mid] > target, search left half.",
            "test_cases": [
                {"input": "5 7\n1 3 5 7 9", "expected": "3", "is_hidden": False},
                {"input": "3 4\n1 2 3", "expected": "-1", "is_hidden": False},
                {"input": "1 1\n1", "expected": "0", "is_hidden": True},
            ],
        },
        {
            "title": "Search the Rotated Safehouse",
            "subtitle": "Search in Rotated Sorted Array",
            "difficulty": "Medium",
            "order": 2,
            "reputation_reward": 250,
            "description": """## Search the Rotated Safehouse

The safehouse addresses were sorted but someone rotated the list. Find the target in this rotated sorted array. Print index or -1.

### Input
- First line: integers N and TARGET
- Second line: N integers (rotated sorted array)

### Output
- Index of target, or -1

### Example
```
Input:
7 0
4 5 6 7 0 1 2

Output:
4
```""",
            "starter_python": "class Solution:\n    def search(self, nums: list[int], target: int) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number}\n */\nvar search = function(nums, target) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Identify which half is sorted by comparing arr[low] with arr[mid].",
            "hint_2": "If target lies in the sorted half, search there; otherwise search the other half.",
            "test_cases": [
                {"input": "7 0\n4 5 6 7 0 1 2", "expected": "4", "is_hidden": False},
                {"input": "7 3\n4 5 6 7 0 1 2", "expected": "-1", "is_hidden": False},
                {"input": "1 1\n1", "expected": "0", "is_hidden": True},
            ],
        },
    ],
    "wiretap-room": [
        {
            "title": "The Anagram Code",
            "subtitle": "Valid Anagram",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## The Anagram Code

Two intercepted messages might be anagrams — same letters, different order. Check if two strings are anagrams of each other.

### Input
- First line: string S
- Second line: string T

### Output
- "true" or "false"

### Example
```
Input:
anagram
nagaram

Output:
true
```""",
            "starter_python": "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write your solution here\n        return false;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public boolean isAnagram(String s, String t) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "starter_js": "/**\n * @param {string} s\n * @param {string} t\n * @return {boolean}\n */\nvar isAnagram = function(s, t) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Count character frequencies for both strings.",
            "hint_2": "If all character counts match, they're anagrams.",
            "test_cases": [
                {"input": "anagram\nnagaram", "expected": "true", "is_hidden": False},
                {"input": "rat\ncar", "expected": "false", "is_hidden": False},
                {"input": "a\na", "expected": "true", "is_hidden": True},
            ],
        },
    ],
    "chain-of-command": [
        {
            "title": "Reverse the Chain",
            "subtitle": "Reverse Linked List",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## Reverse the Chain

The chain of command has been compromised. Reverse the linked list — given space-separated values, print them in reverse order.

### Input
- First line: integer N
- Second line: N space-separated integers

### Output
- Reversed list, space-separated

### Example
```
Input:
5
1 2 3 4 5

Output:
5 4 3 2 1
```""",
            "starter_python": "class Solution:\n    def reverseList(self, nums: list[int]) -> list[int]:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> reverseList(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int[] reverseList(int[] nums) {\n        // Write your solution here\n        return new int[]{};\n    }\n}\n",
            "starter_js": "/**\n * @param {number[]} nums\n * @return {number[]}\n */\nvar reverseList = function(nums) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use three pointers: prev, curr, next.",
            "hint_2": "At each step, reverse the current node's pointer to point to prev.",
            "test_cases": [
                {"input": "5\n1 2 3 4 5", "expected": "5 4 3 2 1", "is_hidden": False},
                {"input": "1\n42", "expected": "42", "is_hidden": False},
                {"input": "3\n10 20 30", "expected": "30 20 10", "is_hidden": True},
            ],
        },
    ],
    "escape-route": [
        {
            "title": "Valid Escape Hatch",
            "subtitle": "Valid Parentheses",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## Valid Escape Hatch

Every escape route has doors that open and close. Check if a string of brackets is properly balanced — every opening bracket must have a matching closing bracket in the correct order.

### Input
- A single string containing only '(', ')', '{', '}', '[', ']'

### Output
- "true" or "false"

### Example
```
Input:
()[]{}

Output:
true
```""",
            "starter_python": "class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValid(string s) {\n        // Write your solution here\n        return false;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public boolean isValid(String s) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "starter_js": "/**\n * @param {string} s\n * @return {boolean}\n */\nvar isValid = function(s) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "Use a stack. Push opening brackets, pop on closing brackets.",
            "hint_2": "When you encounter a closing bracket, check if the top of stack matches.",
            "test_cases": [
                {"input": "()[]{}", "expected": "true", "is_hidden": False},
                {"input": "(]", "expected": "false", "is_hidden": False},
                {"input": "([{}])", "expected": "true", "is_hidden": True},
                {"input": "((", "expected": "false", "is_hidden": True},
            ],
        },
    ],
    "vault": [
        {
            "title": "Climbing the Fire Escape",
            "subtitle": "Climbing Stairs",
            "difficulty": "Easy",
            "order": 1,
            "reputation_reward": 100,
            "description": """## Climbing the Fire Escape

You're escaping via a fire escape with N steps. Each time you can climb 1 or 2 steps. How many distinct ways can you reach the top?

### Input
- A single integer N

### Output
- Number of distinct ways to climb N steps

### Example
```
Input:
3

Output:
3
```

Explanation: 1+1+1, 1+2, 2+1 = 3 ways.""",
            "starter_python": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        # Write your solution here\n        pass\n",
            "starter_cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n",
            "starter_java": "import java.util.*;\n\nclass Solution {\n    public int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "starter_js": "/**\n * @param {number} n\n * @return {number}\n */\nvar climbStairs = function(n) {\n    // Write your solution here\n    \n};\n",
            "hint_1": "This is the Fibonacci sequence! ways(n) = ways(n-1) + ways(n-2).",
            "hint_2": "Use dynamic programming with O(1) space — just track the last two values.",
            "test_cases": [
                {"input": "3", "expected": "3", "is_hidden": False},
                {"input": "5", "expected": "8", "is_hidden": False},
                {"input": "1", "expected": "1", "is_hidden": True},
                {"input": "10", "expected": "89", "is_hidden": True},
            ],
        },
    ],
}

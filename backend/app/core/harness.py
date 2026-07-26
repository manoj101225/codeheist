"""
LeetCode Harness Generator — automatically wraps LeetCode-style solution classes/functions
with input parsing and output rendering drivers for Python, C++, Java, and JavaScript.
"""

def needs_harness(code: str, language: str) -> bool:
    """Check if the user code is LeetCode style (i.e. does NOT contain competitive programming main/input driver)."""
    if language == "python":
        return "input(" not in code and "__main__" not in code
    elif language == "cpp":
        return "main(" not in code
    elif language == "java":
        return "main(" not in code
    elif language == "javascript":
        return "readFileSync" not in code and "process.stdin" not in code
    return False


def apply_harness(code: str, language: str, mission_title: str) -> tuple[str, str]:
    """
    Applies the LeetCode driver harness to user code if needed.
    Returns (wrapped_code, main_class_or_file_name).
    """
    if not needs_harness(code, language):
        return code, "Solution"

    title = mission_title.strip().lower()

    if "crew lineup" in title:
        return _harness_single_array_int_out(code, language, "findMax")
    elif "second-in-command" in title:
        return _harness_single_array_int_out(code, language, "secondLargest")
    elif "two-man job" in title:
        return _harness_array_target_indices_out(code, language, "twoSum")
    elif "zero witness" in title:
        return _harness_single_array_array_out(code, language, "moveZeroes")
    elif "winning streak" in title:
        return _harness_single_array_int_out(code, language, "maxSubArray")
    elif "majority boss" in title:
        return _harness_single_array_int_out(code, language, "majorityElement")
    elif "rotate" in title:
        return _harness_array_k_array_out(code, language, "rotate")
    elif "snitch removal" in title:
        return _harness_remove_duplicates(code, language, "removeDuplicates")
    elif "target acquired" in title or "safehouse" in title:
        return _harness_array_target_int_out(code, language, "search")
    elif "anagram" in title:
        return _harness_two_strings_bool_out(code, language, "isAnagram")
    elif "reverse the chain" in title:
        return _harness_single_array_array_out(code, language, "reverseList")
    elif "escape hatch" in title:
        return _harness_single_string_bool_out(code, language, "isValid")
    elif "fire escape" in title:
        return _harness_single_int_int_out(code, language, "climbStairs")

    return code, "Solution"


def _harness_single_array_int_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        nums = [int(x) for x in tokens[1:1+n]]
        sol = Solution()
        print(getattr(sol, '{method_name}')(nums))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n; if (!(cin >> n)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    cout << sol.{method_name}(nums) << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.{method_name}(nums));
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length === 0 || input[0] === '') return;
    const n = parseInt(input[0]);
    const nums = input.slice(1, 1 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) console.log(fn(nums));
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_array_target_indices_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        target = int(tokens[1])
        nums = [int(x) for x in tokens[2:2+n]]
        sol = Solution()
        res = getattr(sol, '{method_name}')(nums, target)
        if isinstance(res, (list, tuple)):
            print(" ".join(map(str, res)))
        else:
            print(res)
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n, target; if (!(cin >> n >> target)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    auto res = sol.{method_name}(nums, target);
    for (size_t i = 0; i < res.size(); i++) {{
        cout << res[i] << (i + 1 == res.size() ? "" : " ");
    }}
    cout << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int target = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.{method_name}(nums, target);
        for (int i = 0; i < res.length; i++) {{
            System.out.print(res[i] + (i + 1 == res.length ? "" : " "));
        }}
        System.out.println();
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length < 2 || input[0] === '') return;
    const n = parseInt(input[0]);
    const target = parseInt(input[1]);
    const nums = input.slice(2, 2 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) {{
        const res = fn(nums, target);
        console.log(Array.isArray(res) ? res.join(' ') : res);
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_single_array_array_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        nums = [int(x) for x in tokens[1:1+n]]
        sol = Solution()
        res = getattr(sol, '{method_name}')(nums)
        arr = res if res is not None else nums
        print(" ".join(map(str, arr)))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n; if (!(cin >> n)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    auto res = sol.{method_name}(nums);
    for (size_t i = 0; i < res.size(); i++) {{
        cout << res[i] << (i + 1 == res.size() ? "" : " ");
    }}
    cout << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.{method_name}(nums);
        int[] arr = res != null ? res : nums;
        for (int i = 0; i < arr.length; i++) {{
            System.out.print(arr[i] + (i + 1 == arr.length ? "" : " "));
        }}
        System.out.println();
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length === 0 || input[0] === '') return;
    const n = parseInt(input[0]);
    const nums = input.slice(1, 1 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) {{
        const res = fn(nums);
        const arr = Array.isArray(res) ? res : nums;
        console.log(arr.join(' '));
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_array_k_array_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        k = int(tokens[1])
        nums = [int(x) for x in tokens[2:2+n]]
        sol = Solution()
        res = getattr(sol, '{method_name}')(nums, k)
        arr = res if res is not None else nums
        print(" ".join(map(str, arr)))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n, k; if (!(cin >> n >> k)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    auto res = sol.{method_name}(nums, k);
    for (size_t i = 0; i < res.size(); i++) {{
        cout << res[i] << (i + 1 == res.size() ? "" : " ");
    }}
    cout << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int[] res = sol.{method_name}(nums, k);
        int[] arr = res != null ? res : nums;
        for (int i = 0; i < arr.length; i++) {{
            System.out.print(arr[i] + (i + 1 == arr.length ? "" : " "));
        }}
        System.out.println();
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length < 2 || input[0] === '') return;
    const n = parseInt(input[0]);
    const k = parseInt(input[1]);
    const nums = input.slice(2, 2 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) {{
        const res = fn(nums, k);
        const arr = Array.isArray(res) ? res : nums;
        console.log(arr.join(' '));
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_remove_duplicates(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        nums = [int(x) for x in tokens[1:1+n]]
        sol = Solution()
        res = getattr(sol, '{method_name}')(nums)
        if isinstance(res, tuple):
            k, nums = res
        else:
            k = res
        print(k)
        print(" ".join(map(str, nums[:k])))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n; if (!(cin >> n)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    int k = sol.{method_name}(nums);
    cout << k << "\\n";
    for (int i = 0; i < k; i++) {{
        cout << nums[i] << (i + 1 == k ? "" : " ");
    }}
    cout << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        int k = sol.{method_name}(nums);
        System.out.println(k);
        for (int i = 0; i < k; i++) {{
            System.out.print(nums[i] + (i + 1 == k ? "" : " "));
        }}
        System.out.println();
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length === 0 || input[0] === '') return;
    const n = parseInt(input[0]);
    const nums = input.slice(1, 1 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) {{
        const k = fn(nums);
        console.log(k);
        console.log(nums.slice(0, k).join(' '));
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_array_target_int_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        target = int(tokens[1])
        nums = [int(x) for x in tokens[2:2+n]]
        sol = Solution()
        print(getattr(sol, '{method_name}')(nums, target))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int n, target; if (!(cin >> n >> target)) return 0;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    Solution sol;
    cout << sol.{method_name}(nums, target) << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        int target = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.{method_name}(nums, target));
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const input = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (!input || input.length < 2 || input[0] === '') return;
    const n = parseInt(input[0]);
    const target = parseInt(input[1]);
    const nums = input.slice(2, 2 + n).map(Number);
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) console.log(fn(nums, target));
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_two_strings_bool_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    lines = [l.strip() for l in sys.stdin if l.strip()]
    if len(lines) >= 2:
        s, t = lines[0], lines[1]
        sol = Solution()
        res = getattr(sol, '{method_name}')(s, t)
        print("true" if res else "false")
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    string s, t;
    if (!(cin >> s >> t)) return 0;
    Solution sol;
    cout << (sol.{method_name}(s, t) ? "true" : "false") << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String s = sc.next(), t = sc.next();
        Solution sol = new Solution();
        System.out.println(sol.{method_name}(s, t) ? "true" : "false");
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const lines = fs.readFileSync(0, 'utf8').trim().split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);
    if (lines.length >= 2) {{
        const s = lines[0], t = lines[1];
        const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
        if (fn) console.log(fn(s, t) ? "true" : "false");
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_single_string_bool_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    s = sys.stdin.read().strip()
    sol = Solution()
    res = getattr(sol, '{method_name}')(s)
    print("true" if res else "false")
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    string s;
    if (!(cin >> s)) return 0;
    Solution sol;
    cout << (sol.{method_name}(s) ? "true" : "false") << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        String s = sc.next();
        Solution sol = new Solution();
        System.out.println(sol.{method_name}(s) ? "true" : "false");
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const s = fs.readFileSync(0, 'utf8').trim();
    const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
    if (fn) console.log(fn(s) ? "true" : "false");
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"


def _harness_single_int_int_out(code: str, lang: str, method_name: str) -> tuple[str, str]:
    if lang == "python":
        driver = f"""
if __name__ == '__main__':
    import sys
    tokens = sys.stdin.read().split()
    if tokens:
        n = int(tokens[0])
        sol = Solution()
        print(getattr(sol, '{method_name}')(n))
"""
        return code + "\n" + driver, "Solution"
    elif lang == "cpp":
        driver = f"""
int main() {{
    int n; if (!(cin >> n)) return 0;
    Solution sol;
    cout << sol.{method_name}(n) << "\\n";
    return 0;
}}
"""
        return code + "\n" + driver, "Solution"
    elif lang == "java":
        driver = f"""
class SolutionRunner {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();
        Solution sol = new Solution();
        System.out.println(sol.{method_name}(n));
    }}
}}
"""
        return code + "\n" + driver, "SolutionRunner"
    elif lang == "javascript":
        driver = f"""
(function() {{
    const fs = require('fs');
    const tokens = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);
    if (tokens && tokens[0]) {{
        const n = parseInt(tokens[0]);
        const fn = typeof {method_name} !== 'undefined' ? {method_name} : (typeof Solution !== 'undefined' ? (new Solution()).{method_name} : null);
        if (fn) console.log(fn(n));
    }}
}})();
"""
        return code + "\n" + driver, "Solution"
    return code, "Solution"

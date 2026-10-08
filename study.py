# Question 1: Repeatedly Delete Leaves Matching a Target Value
# Practice version: input and output are TreeNode objects.

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def remove_target_leaves(root, target):
    # TODO: Write your solution here.
    def isleaf(node):
    	return node.left == None and node.right == None

    def dfs(node, target):
    	if not node:
    		return None

    	ldfs = dfs(node.left, target)
    	rdfs = dfs(node.right, target)

    	node.left = ldfs
    	node.right = rdfs

    	if isleaf(node) and node.val == target:
    		return None

    	return node

    return dfs(root, target)




def remove_target_leaves_iterative(root, target):
    # A leaf has neither a left child nor a right child.
    def isleaf(node):
        return node.left is None and node.right is None

    # Create an extra parent. Its left link holds the real root.
    # The dummy's value 0 does not matter: we never process the dummy.
    dummy = TreeNode(0, left = root)

    # Each task is (current node, its parent, isready).
    # False = first visit; schedule children before checking this node.
    # True = return visit; children are cleaned, so check this node now.
    # The stack starts with ONE task for the real root.
    stack = [(root, dummy, False)]

    # Repeat until no tasks remain. The size can grow or shrink.
    while len(stack) != 0:
        # Pop EXACTLY ONE tuple per iteration, from the END of the list.
        # These names refer to the three items in that one tuple.
        node, parent, isready = stack.pop()

        # Missing children still have tasks, but require no work.
        # Pop one, add nothing to the stack, then immediately start the next iteration.
        if node == None:
            continue

        if not isready:
            # First visit: pop one task, then add THREE tasks.
            # Net change in the stack size this iteration: +2.
            # The saved task below does NOT say children are finished now.
            # It says: check this node WHEN this task is popped later.
            stack.append((node, parent, True))

            # Schedule right, then left. Each child's parent is this node.
            # Last added comes out first, so LEFT runs before RIGHT.
            # Both subtrees finish before the saved True task comes out.
            stack.append((node.right, node, False))
            stack.append((node.left, node, False))

        else:
            # Return visit: pop one task and add nothing to the stack.
            # Children have finished, so check their UPDATED links.
            if isleaf(node) and node.val == target:
                # Clear only the parent's link to this node.
                # With this TreeNode class, == compares object identity.
                if parent.left == node:
                    parent.left = None
                else:
                    parent.right = None
            # A surviving node needs no action: its parent's link stays.

    # This is AFTER the entire loop, not after an individual iteration.
    # If the root was deleted, dummy.left is now None.
    return dummy.left


# FULL WALKTHROUGH FOR THE ITERATIVE FUNCTION ABOVE
# This example is DIFFERENT from the 7-with-children-7-and-3 sample below.
# target = 7; a chain of three distinct nodes, all with value 7:
#
#       dummy (value 0, never checked)
#       /
#     top (7)
#     /
#   middle (7)
#   /
# bottom (7)
#
# "top", "middle", and "bottom" are explanatory names for NODE OBJECTS,
# not new variables you must add. They distinguish the three equal sevens.
# All right children are None. Bottom's left child is also None.
#
# In every stack shown below:
# - LEFT end = bottom of stack; RIGHT end = next task to pop.
# - F means False (first visit); T means True (check after children).
# - Each (...) is ONE tuple/task, containing node, parent, and flag.
# - Each iteration pops EXACTLY ONE tuple.
#
# INITIAL STACK, size 1:
# [(top, dummy, F)]
#
# ITERATION 1: pop (top, dummy, F). Stack is temporarily empty.
# Process top's first visit. Add these THREE tasks, in this order:
#   (top, dummy, T), (None, top, F), (middle, top, F)
# END STACK, size 3:
# [(top, dummy, T), (None, top, F), (middle, top, F)]
# Tree unchanged. Next task: middle's first visit.
#
# ITERATION 2: pop (middle, top, F). TWO older tasks remain.
# Add THREE: (middle, top, T), (None, middle, F), (bottom, middle, F)
# END STACK, size 5:
# [(top, dummy, T), (None, top, F), (middle, top, T),
#  (None, middle, F), (bottom, middle, F)]
# Tree unchanged. Next task: bottom's first visit.
#
# ITERATION 3: pop (bottom, middle, F). FOUR older tasks remain.
# Add THREE: (bottom, middle, T), (None, bottom, F), (None, bottom, F)
# The two None tasks mean right missing child, then left missing child.
# END STACK, size 7:
# [(top, dummy, T), (None, top, F), (middle, top, T),
#  (None, middle, F), (bottom, middle, T),
#  (None, bottom, F), (None, bottom, F)]
# Tree unchanged. Next task: bottom's missing LEFT child.
#
# ITERATION 4: pop (None, bottom, F), the missing LEFT child.
# Add nothing to the stack. "continue" skips all further work for this task.
# END STACK, size 6:
# [(top, dummy, T), (None, top, F), (middle, top, T),
#  (None, middle, F), (bottom, middle, T), (None, bottom, F)]
#
# ITERATION 5: pop (None, bottom, F), the missing RIGHT child.
# Add nothing to the stack. Skip this task too.
# END STACK, size 5:
# [(top, dummy, T), (None, top, F), (middle, top, T),
#  (None, middle, F), (bottom, middle, T)]
# Next task: check bottom itself. Both child tasks are finished.
#
# ITERATION 6: pop (bottom, middle, T). Add nothing to the stack.
# Bottom is a leaf with value 7, so clear middle.left.
# Middle NOW becomes a leaf, but we do not check it in this iteration.
# END STACK, size 4:
# [(top, dummy, T), (None, top, F), (middle, top, T),
#  (None, middle, F)]
# Next task: middle's missing RIGHT child.
#
# ITERATION 7: pop (None, middle, F). Add nothing to the stack. Skip it.
# END STACK, size 3:
# [(top, dummy, T), (None, top, F), (middle, top, T)]
#
# ITERATION 8: pop (middle, top, T). Add nothing to the stack.
# Middle is now a leaf with value 7, so clear top.left.
# Top NOW becomes a leaf; its check is still waiting in the stack.
# END STACK, size 2:
# [(top, dummy, T), (None, top, F)]
#
# ITERATION 9: pop (None, top, F). Add nothing to the stack. Skip it.
# END STACK, size 1:
# [(top, dummy, T)]
#
# ITERATION 10: pop (top, dummy, T). Add nothing to the stack.
# Top is now a leaf with value 7, so clear dummy.left.
# END STACK, size 0: []
#
# The while condition is now false. Return dummy.left, which is None.
# TOTAL: 10 iterations, 10 pops, 9 tasks added inside the loop,
# plus the 1 initial task. All three real nodes were deleted.
# First visits grow the stack; missing-child and return visits shrink it.


if __name__ == "__main__":
    #       7
    #      / \
    #     7   3
    root = TreeNode(7, TreeNode(7), TreeNode(3))
    target = 7

    result = remove_target_leaves(root, target)
    # Expected: the root 7 stays, its left child disappears,
    # and its right child 3 stays.


# =====================================================================
# QUESTION 2: Infection Spread on a Grid (Cellular Automaton)
# COMPLETED PRACTICE QUESTION
# Baseline: copy then scan every cell and its four neighbors. For ONE
# step this is already O(R*C) time and space.
# For many steps, repeated full scans cost O(steps*R*C); a BFS frontier
# can avoid rescanning unchanged cells. We will study that extension later.
# =====================================================================
# We start with the PDF's supplied solution and sample cases: ONE step.
# Input: a rectangular list of strings; H = healthy, I = infected.
# A healthy cell becomes infected if a neighbor ABOVE, BELOW, LEFT,
# or RIGHT was infected at the START of this step. No diagonal spread.
# All changes happen simultaneously: newly infected cells do not spread
# again during the same step. Return the resulting list of strings.
# Existing infected cells stay infected. Empty input returns [].
# Multi-step spread and recovery are extensions to study afterward.


def infection_spread_one_step(grid: list[str]) -> list[str]:
    def inbounds(r,c):
        return 0<= r < len(grid) and 0<=c < len(grid[0])
    if not grid:
        return []

    rows, cols = len(grid), len(grid[0])
    ans = [list(row) for row in grid]



    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'H':
                continue

            for dr,dc in ((1,0), (-1,0),(0,1),(0,-1)):
                nr = dr+r
                nc = dc+c

                if inbounds(nr,nc) and grid[nr][nc] == 'H':
                    ans[nr][nc] = "I"

    ans = [''.join(row) for row in ans]
    return ans






# Sample 1:
# Input:    ["HHH", "HIH", "HHH"]
# Expected: ["HIH", "III", "HIH"]
#
# Sample 2:
# Input:    ["HHH"]
# Expected: ["HHH"]
#
# Sample 3 (shows why newly infected cells must wait until the next step):
# Input:    ["IHH"]
# Expected: ["IIH"]
#
# When your solution is ready, try:
# print(infection_spread_one_step(["HHH", "HIH", "HHH"]))


# QUESTION 2: Interview reference - one simultaneous spread step.
# Read from grid; write to result. Time and space: O(rows * cols).
def infection_spread_one_step_reference(grid):
    if not grid:
        return []

    rows = len(grid)
    cols = len(grid[0])
    result = [list(row) for row in grid]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "I":
                continue

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == "H":
                        result[nr][nc] = "I"

    return ["".join(row) for row in result]


# COMPARISON WITH YOUR SOLUTION ABOVE
# Correctness: both produce the same one-step grid and preserve the input.
# Efficiency: both O(rows * cols) time and space; no algorithmic upgrade needed.
# Your inbounds helper is a good way to name and reuse the boundary check.
# Optional: define it after rows/cols and use those names instead of len(grid).
# Your "skip H" is correct for H/I input. "Skip anything that is not I"
# makes the spreading rule explicit, useful if barriers are later introduced.
# That alone does not implement recovery or other follow-up state rules.
# Your separate conversion and return are correct and easy to read.
# The reference combines them into one return; shorter is not always clearer.
# Optional clarity: result or next_grid describes the copy better than ans.
# Add spaces around operators and after commas; remove extra blank lines and
# the stale TODO once satisfied. These are readability changes, not bug fixes.
# Key rule: read the ORIGINAL to decide which cells may spread this step.
# The healthy-neighbor test can read original or copy in this H/I version;
# updating an already infected neighbor again makes no difference.


# =====================================================================
# QUESTION 1: Repeatedly Delete Leaves Matching a Target Value
# =====================================================================
# Tree-node interface, as we practiced. The PDF's main interface is a
# level-order list; that interface additionally needs decoding and encoding.
# Brute force: repeatedly scan and delete current matching leaves.
# Time O(n * h), worst O(n^2); DFS scan space O(h).
# Better: children first, then decide whether the parent is now deletable.
# Time O(n); extra space O(h). Return None to delete, or node to keep.


def remove_target_leaves_reference(root, target):
    if root is None:
        return None
    root.left = remove_target_leaves_reference(root.left, target)
    root.right = remove_target_leaves_reference(root.right, target)
    if root.left is None and root.right is None and root.val == target:
        return None
    return root


# Example: root 7 with left child 7 and right child 3 => keep root and 3.
# Your own recursive and iterative solutions remain in study.py.


# =====================================================================
# QUESTION 3: Find minimum threshold enabling grid path
# =====================================================================
# Four-direction path from top-left to bottom-right.
# Path cost = largest CELL VALUE visited, including the start.
# This differs from the follow-up minimizing adjacent height differences.
# Brute force: enumerate simple paths, exponential time, O(R*C) space.
# Better: Dijkstra, with max instead of addition when extending a path.
# Time O(R*C log(R*C)); space O(R*C). Empty grid returns 0 here.
# Heap task: (best maximum so far, row, column).
from heapq import heappush, heappop
def minimum_grid_threshold(grid):
    def inbounds(r,c):
        return 0<= r < len(grid) and 0<=c<len(grid[0])

    dirs = [(1,0),(0,1), (-1,0),(0,-1)]

    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    best = [[float('inf')]* cols for r in range(rows)]
    best[0][0] = grid[0][0]
    heap = [(best[0][0],0,0)]
    while heap:
        score, r,c = heappop(heap)
        if best[r][c] !=  score:
            continue

        if (r,c) == (rows-1, cols-1):
            return score

        for dr,dc in dirs:
            nr,nc = r+dr, c+dc
            if inbounds(nr, nc):
                newscore = max(grid[nr][nc], score)
                if newscore < best[nr][nc]:
                    best[nr][nc] = newscore

                    heappush(heap, (newscore, nr,nc))


# Example: minimum_grid_threshold([[0,2],[1,3]]) => 3
# Questions 3, 5 part 1, and 7 use the same maximum-cell pattern.


# QUESTION 3: REFERENCE FOR COMPARISON
# Both solutions use the same algorithm and have the same complexity:
# time O(R*C log(R*C)), space O(R*C).
# Your inbounds helper and separate dirs list are useful readability choices.
# score/newscore and cost/new_cost are equivalent names, not logic differences.
# max(height, score) equals max(score, height): argument order does not matter.
# Compare: calculate this route with MAX, then accept a SMALLER neighbor score.
# Keep score first in heap tuples; record best before pushing the new task.
# Optional polish: consistent spaces, remove the stale practice comment, and
# keep heap imports once at the top (they are already there).

def minimum_grid_threshold_reference(grid):
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        cost, r, c = heappop(heap)
        if cost != best[r][c]:
            continue  # An older task was replaced by a better route.
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = max(cost, grid[nr][nc])
                if new_cost < best[nr][nc]:
                    best[nr][nc] = new_cost
                    heappush(heap, (new_cost, nr, nc))


# QUESTION 3: SIMPLE ASSERT TESTS FOR INTERVIEW DAY
# Choose an input, work out its expected answer by hand, then assert equality.
# If an assert is false, Python stops with AssertionError at that test.
# Cover a normal case, the smallest input, and a tricky route; explain why.
# Empty-grid tests apply to our agreed convention that the answer is 0.
# Run this file to execute the assertions below.
if __name__ == "__main__":
    # Normal case: both routes have largest value 3.
    assert minimum_grid_threshold([[0, 2], [1, 3]]) == 3

    # Smallest grid: its starting cell is also the goal.
    assert minimum_grid_threshold([[7]]) == 7

    # Tricky route: go around 100; the best route's largest value is 2.
    assert minimum_grid_threshold([[0, 100, 2],
                                   [1,   2, 2],
                                   [3,   4, 1]]) == 2

    # One row: the middle cell cannot be avoided.
    assert minimum_grid_threshold([[1, 8, 2]]) == 8

    # One column: every cell is required.
    assert minimum_grid_threshold([[1], [6], [2]]) == 6

    # Equal heights: the limit equals that shared height.
    assert minimum_grid_threshold([[4, 4], [4, 4]]) == 4

    # Empty inputs: the convention used in our practice solution.
    assert minimum_grid_threshold([]) == 0
    assert minimum_grid_threshold([[]]) == 0

    print("All question-three tests passed.")


# QUESTION 3: REVISION NOTES FROM OUR DISCUSSION
# A min-heap of tuples compares the first item first: put the priority score
# before row/column; coordinates break ties. A stale entry is an old task
# whose score no longer matches best[r][c]; skip it to avoid redundant work.
# The route score is a MAX within a path; choose the MIN across possible paths.
# best can be a rectangular table or a dictionary keyed by (row, column).
# A table is straightforward for a dense grid. A dictionary stores discovered
# cells only, but keys and hash-table bookkeeping add overhead per entry.
# Both have O(R*C) worst-case storage; a sparse dictionary may store fewer cells.
# [[1], [6], [2]] is three rows, one column: only route 1 -> 6 -> 2, answer 6.
# Passing a grid literal directly to a function is valid; name it when helpful.

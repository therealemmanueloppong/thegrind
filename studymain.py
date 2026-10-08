# READ FIRST: THE MOST COMMON PATTERN IN THESE NINE QUESTIONS
# Dijkstra appears most often: questions 3, 5, 6, and 7.
# Start by asking: "What makes one path better than another?"
# - Grid threshold / maximum height: path cost is the largest cell visited.
#   Extending a path uses max(current_cost, next_cell_height).
# - Network delay / travel: path cost is total travel time.
#   Extending a path uses current_cost + edge_weight.
# The shared steps: store the best cost for each position, use a min-heap
# to take the smallest pending cost, skip outdated tasks, and add a new
# task only when a neighbor's best cost improves. Assume nonnegative weights.
# A normal BFS queue suits equal-cost steps; a heap suits weighted costs.
# Other patterns: children-first DFS for leaf deletion; two DFS passes for
# tree distance sums; preorder + child counts for encoding; union-find for
# friend-only connectivity. Unfriend events need a different approach.
# Learn the cost rule and traversal order first, then rebuild the code.

# HARD SECTION 1: BFS/DFS, Graph & Tree Traversal, Shortest Paths
# Hard questions in the PDF's order. Current question: 3.
# Completed question 2 is archived with its notes in study.py.
# Keep these references to read, then delete a function's body and rebuild it.
# When satisfied, copy the completed question into study.py for revision.
# These are the main problems; extra follow-ups are labeled separately.
# Short recursive examples use O(height) call-stack space and may need an
# iterative version for deep trees. Weighted paths assume nonnegative weights.

from collections import defaultdict
from heapq import heappop, heappush


# =====================================================================
# QUESTION 1: Repeatedly Delete Leaves Matching a Target Value
# =====================================================================
# Tree-node interface, as we practiced. The PDF's main interface is a
# level-order list; that interface additionally needs decoding and encoding.
# Brute force: repeatedly scan and delete current matching leaves.
# Time O(n * h), worst O(n^2); DFS scan space O(h).
# Better: children first, then decide whether the parent is now deletable.
# Time O(n); extra space O(h). Return None to delete, or node to keep.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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
def minimum_grid_threshold(grid):
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


# Example: minimum_grid_threshold([[0,2],[1,3]]) => 3
# Questions 3, 5 part 1, and 7 use the same maximum-cell pattern.


# =====================================================================
# QUESTION 4: Compute distance-sum from every tree node
# =====================================================================
# Input: n nodes labeled 0..n-1, undirected edges forming a tree.
# Output: sum of distances from each node to all other nodes.
# Brute force: BFS from each node, O(n^2) time and O(n) space.
# Better: two DFS passes, O(n) time and O(n) space including adjacency.
# First pass: subtree sizes and root's distance sum.
# Second pass: moving into a child's subtree makes size[child] nodes
# one step closer and the other n-size[child] nodes one step farther.
def tree_distance_sums(n, edges):
    if n == 0:
        return []
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    size = [1] * n
    answer = [0] * n

    def collect(node, parent):
        for child in graph[node]:
            if child == parent:
                continue
            collect(child, node)
            size[node] += size[child]
            answer[node] += answer[child] + size[child]

    def reroot(node, parent):
        for child in graph[node]:
            if child == parent:
                continue
            answer[child] = answer[node] - size[child] + (n - size[child])
            reroot(child, node)

    collect(0, -1)
    reroot(0, -1)
    return answer


# Example: tree_distance_sums(4, [(0,1),(1,2),(1,3)]) => [5,3,5,5]


# =====================================================================
# QUESTION 5: Compute minimax grid path and network delay
# =====================================================================
# Part 1. Four-direction path from top-left to bottom-right.
# Path cost = largest CELL VALUE visited, including the start.
# This differs from the follow-up minimizing adjacent height differences.
# Brute force: enumerate simple paths, exponential time, O(R*C) space.
# Better: Dijkstra, with max instead of addition when extending a path.
# Time O(R*C log(R*C)); space O(R*C). Empty grid returns 0 here.
# Heap task: (best maximum so far, row, column).
def minimax_grid_path(grid):
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


# Example: minimax_grid_path([[0,2],[1,3]]) => 3
# Questions 3, 5 part 1, and 7 use the same maximum-cell pattern.


# QUESTION 5, PART 2: Network delay
# Directed edges (a,b,time), nodes labeled 1..n, starting node source.
# Return time until everyone receives the signal, or -1 if unreachable.
# Brute force: Bellman-Ford, O(V*E) time and O(V) distance storage.
# Better: Dijkstra; shortest distances use ADDITION, unlike the grid MAX.
# Time O((V+E) log V) for simple graphs; space O(V+E).
# With arbitrary parallel edges, a lazy heap can take O(E log E) time.
def network_delay(times, n, source):
    graph = defaultdict(list)
    for a, b, weight in times:
        graph[a].append((b, weight))
    distances = {}
    heap = [(0, source)]
    while heap:
        cost, node = heappop(heap)
        if node in distances:
            continue
        distances[node] = cost  # First pop settles this node's shortest time.
        for neighbor, weight in graph[node]:
            if neighbor not in distances:
                heappush(heap, (cost + weight, neighbor))
    return max(distances.values()) if len(distances) == n else -1


# Example: network_delay([(2,1,1),(2,3,1),(3,4,1)], 4, 2) => 2


# =====================================================================
# QUESTION 6: Minimize travel time with optional meeting point
# =====================================================================
# PDF's assumed rules: nodes 0..n-1, nonnegative weights, two travelers.
# They meet when the later traveler arrives, then travel together to dest.
# Return [minimum arrival time, meeting node]; smallest node breaks ties.
# Meeting at dest already includes the option of traveling separately.
# Brute force: all-pairs shortest paths, O(V^3) time, O(V^2) space.
# Better: three Dijkstra searches. The reversed graph gives distances TO dest.
# Time O((V+E) log V) for a simple graph; space O(V+E).
def best_meeting_point(n, edges, start_a, start_b, dest, directed=False):
    if n <= 0:
        return [-1, -1]
    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for a, b, weight in edges:
        graph[a].append((b, weight))
        reverse[b].append((a, weight))
        if not directed:
            graph[b].append((a, weight))
            reverse[a].append((b, weight))

    def distances(start, adjacency):
        dist = [float("inf")] * n
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            cost, node = heappop(heap)
            if cost != dist[node]:
                continue
            for neighbor, weight in adjacency[node]:
                new_cost = cost + weight
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    heappush(heap, (new_cost, neighbor))
        return dist

    from_a = distances(start_a, graph)
    from_b = distances(start_b, graph)
    to_dest = distances(dest, reverse)
    best_time = float("inf")
    best_node = -1
    for node in range(n):
        time = max(from_a[node], from_b[node]) + to_dest[node]
        if time < best_time:
            best_time = time
            best_node = node
    # Ascending node order preserves the smallest node on equal finite times.
    return [best_time, best_node] if best_node != -1 else [-1, -1]


# Example: best_meeting_point(4, [(0,1,2),(1,2,1),(1,3,2),(2,3,2)],
#                            0, 2, 3) => [4,1]


# =====================================================================
# QUESTION 7: Minimize maximum height along a grid path
# =====================================================================
# Four-direction path from top-left to bottom-right.
# Path cost = largest CELL VALUE visited, including the start.
# This differs from the follow-up minimizing adjacent height differences.
# Brute force: enumerate simple paths, exponential time, O(R*C) space.
# Better: Dijkstra, with max instead of addition when extending a path.
# Time O(R*C log(R*C)); space O(R*C). Empty grid returns 0 here.
# Heap task: (best maximum so far, row, column).
def minimum_maximum_height(heights):
    if not heights or not heights[0]:
        return 0
    rows = len(heights)
    cols = len(heights[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = heights[0][0]
    heap = [(heights[0][0], 0, 0)]
    while heap:
        cost, r, c = heappop(heap)
        if cost != best[r][c]:
            continue  # An older task was replaced by a better route.
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = max(cost, heights[nr][nc])
                if new_cost < best[nr][nc]:
                    best[nr][nc] = new_cost
                    heappush(heap, (new_cost, nr, nc))


# Example: minimum_maximum_height([[0,2],[1,3]]) => 3
# Questions 3, 5 part 1, and 7 use the same maximum-cell pattern.


# =====================================================================
# QUESTION 8: Encode and decode a general N-ary tree
# =====================================================================
# Simple learning version: INTEGER values, ordered children, valid input.
# Encode in preorder as pairs: value, child_count. Empty tree => "".
# Brute force: recursively construct nested bracket strings; repeated
# copying can take O(n*h) time. A list of tokens avoids repeated copying.
# Time/space O(n) with bounded-size values; O(L) for serialized text length L.
# Recursive call depth O(h); use an explicit stack for very deep trees.
class NaryNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children


def encode_nary(root):
    tokens = []

    def visit(node):
        tokens.append(str(node.val))
        tokens.append(str(len(node.children)))
        for child in node.children:
            visit(child)

    if root is not None:
        visit(root)
    return " ".join(tokens)


def decode_nary(data):
    if not data:
        return None
    tokens = iter(data.split())

    def build():
        value = int(next(tokens))
        child_count = int(next(tokens))
        node = NaryNode(value)
        for _ in range(child_count):
            node.children.append(build())
        return node

    return build()


# Example: root 1 with children 2 and 3 => "1 2 2 0 3 0".
# Arbitrary string values need JSON or length-prefixing instead of splitting.


# =====================================================================
# QUESTION 9: Friend Graph with Timeline (Friend / Unfriend Events)
# =====================================================================
# BASE: friend events only, people labeled 0..n-1.
# Event: (time, person_a, person_b, "friend"). Return earliest time
# everyone is connected, or -1. One person is connected at time 0.
# Brute force: replay events and DFS at every timestamp, O(T*(N+E)).
# Better base: sorted events + union-find, O(E log E + E*alpha(N) + N)
# time. Space O(N+E), including the sorted copy of events.
# Reject deletion events: ignoring them would give an incorrect answer.
def earliest_all_connected(n, events):
    if any(kind != "friend" for _, _, _, kind in events):
        raise ValueError("Use the unfriend version for deletion events")
    if n <= 1:
        return 0
    parent = list(range(n))
    size = [1] * n
    components = n

    def find(person):
        while parent[person] != person:
            parent[person] = parent[parent[person]]
            person = parent[person]
        return person

    for time, a, b, kind in sorted(events, key=lambda event: event[0]):
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            continue
        if size[root_a] < size[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        size[root_a] += size[root_b]
        components -= 1
        if components == 1:
            return time
    return -1


# Example: earliest_all_connected(3, [(1,0,1,"friend"),
#                                    (5,1,2,"friend")]) => 5


# QUESTION 9 FOLLOW-UP: simple working version supporting unfriend.
# Update adjacency, then DFS after all events at the same timestamp.
# Same-time events are applied in input order; check the final state at time t.
# Time O(E log E + T*(N+E)); space O(N+E), T = distinct timestamps.
# This is a baseline, not the optimal dynamic-connectivity solution.
# The faster offline method uses edge lifetimes + rollback union-find.
def earliest_all_connected_with_unfriend(n, events):
    if n <= 1:
        return 0
    graph = [set() for _ in range(n)]
    ordered = sorted(events, key=lambda event: event[0])
    i = 0
    while i < len(ordered):
        time = ordered[i][0]
        while i < len(ordered) and ordered[i][0] == time:
            _, a, b, kind = ordered[i]
            if kind == "friend":
                graph[a].add(b)
                graph[b].add(a)
            elif kind == "unfriend":
                graph[a].discard(b)
                graph[b].discard(a)
            else:
                raise ValueError("Unknown event kind")
            i += 1
        seen = {0}
        stack = [0]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) == n:
            return time
    return -1

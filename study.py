"""Google: 1Point3Acres / asked in the last 30 days / PDF questions 1–16.

Reference solutions in the latest PDF's strict date order (October 10, 2026).
This is the revision/reference file. studymain.py remains empty for practice.
Read a question's contract before learning its code. Related interview reports
sometimes describe different tasks: the concrete variants below are labeled.
Unspecified nested-course grouping, server-job rules, and online deletions need
clarification; a generic solution cannot determine those missing rules.

Patterns: Union-Find joins groups; BFS counts equal-cost steps; Dijkstra chooses
weighted/bottleneck paths; sweep lines count overlaps; rolling DP counts paths;
tries share prefixes; dictionaries and deques maintain streaming state.
All examples/tests run only when this file is executed directly.
"""
from collections import Counter, defaultdict, deque
from bisect import bisect_left, bisect_right
from heapq import heappop, heappush, nsmallest
from math import atan2, pi, inf

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


# 01. Friend Graph with Timeline (Friend / Unfriend Events)
# Base: n people numbered 0..n-1; (time, a, b, "friend") events only.
# Return earliest connected time, -1 if never; n <= 1 convention: 0.
# Idea: each successful union reduces the number of groups by one.
# Time: O(n + E log E + E*alpha(n)). Space: O(n + E), including sorting.
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, node):
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.groups -= 1
        return True


def earliest_all_connected(n, events):
    if n <= 1:
        return 0
    uf = UnionFind(n)
    for time, a, b, action in sorted(events, key=lambda event: event[0]):
        if action != "friend":
            raise ValueError("Use the offline version for unfriend events")
        uf.union(a, b)
        if uf.groups == 1:
            return time
    return -1


# Concrete follow-up: friend/unfriend, all events known beforehand.
# Evaluate the graph AFTER all events at each timestamp (input order breaks ties).
# Segment tree stores each edge's active interval; rollback restores group state.
# Duplicate friend and nonexistent unfriend are ignored. Self edges are harmless.
# Time O(n + E log E log n); space O(n + E log E).
def earliest_connected_with_unfriend(n, events, return_counts=False):
    if n <= 1 and not return_counts:
        return 0
    times = sorted({event[0] for event in events})
    if not times:
        return [] if return_counts else -1
    counts = [0]*len(times)
    index = {time: i for i, time in enumerate(times)}
    active, intervals = {}, []
    for time, a, b, action in sorted(events, key=lambda event: event[0]):
        edge = tuple(sorted((a, b)))
        if action == "friend":
            active.setdefault(edge, index[time])
        elif action == "unfriend":
            if edge in active:
                intervals.append((active.pop(edge), index[time], edge))
        else:
            raise ValueError("Unknown action")
    intervals.extend((start, len(times), edge) for edge, start in active.items())
    tree = [[] for _ in range(4 * len(times))]

    def store(node, lo, hi, start, end, edge):
        if end <= lo or hi <= start:
            return
        if start <= lo and hi <= end:
            tree[node].append(edge)
            return
        mid = (lo + hi) // 2
        store(2 * node, lo, mid, start, end, edge)
        store(2 * node + 1, mid, hi, start, end, edge)

    for start, end, edge in intervals:
        if start < end:
            store(1, 0, len(times), start, end, edge)
    parent, size = list(range(n)), [1] * n
    groups, history = n, []

    def root(node):
        # No path compression: every change must be undoable.
        while parent[node] != node:
            node = parent[node]
        return node

    def walk(node, lo, hi):
        nonlocal groups
        mark = len(history)
        for a, b in tree[node]:
            a, b = root(a), root(b)
            if a == b:
                continue
            if size[a] < size[b]:
                a, b = b, a
            history.append((a, b, size[a]))
            parent[b] = a
            size[a] += size[b]
            groups -= 1
        answer = -1
        if hi - lo == 1:
            counts[lo] = groups
            if groups == 1:
                answer = times[lo]
        else:
            mid = (lo + hi) // 2
            answer = walk(2 * node, lo, mid)
            if answer == -1 or return_counts:
                right_answer = walk(2 * node + 1, mid, hi)
                if answer == -1:
                    answer = right_answer
        while len(history) > mark:
            a, b, old_size = history.pop()
            parent[b] = b
            size[a] = old_size
            groups += 1
        return answer

    earliest = walk(1, 0, len(times))
    return list(zip(times, counts)) if return_counts else earliest


# Number of groups after all events at each timestamp; supports deletions too.
def friendship_group_counts(n, events):
    return earliest_connected_with_unfriend(n, events, return_counts=True)


# Past-time connectivity, FRIEND-ONLY: sort queries and events together.
# queries = (time, a, b); answers keep the original query order.
# Simpler than a persistent union tree. O(E log E + Q log Q + (E+Q)*alpha(n)).
def connected_at_times(n, events, queries):
    events = sorted(events, key=lambda event: event[0])
    uf, answers, i = UnionFind(n), [False] * len(queries), 0
    for q, (time, a, b) in sorted(enumerate(queries), key=lambda item: item[1][0]):
        while i < len(events) and events[i][0] <= time:
            _, x, y, action = events[i]
            if action != "friend":
                raise ValueError("This query version assumes friend-only events")
            uf.union(x, y)
            i += 1
        answers[q] = uf.find(a) == uf.find(b)
    return answers



# 02. Maximum-Area Rectangle from Planar Points (rotation allowed)
# Rectangles have equal-length diagonals with the same midpoint.
# Simple bucket version: O(P^2 + sum(bucket_size^2)) time, O(P^2) space.
# Cross products compute the area exactly for integer coordinates.
def maximum_rectangle_area(points):
    points = list(set(map(tuple, points)))
    buckets = defaultdict(list)
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1:]:
            key = (x1 + x2, y1 + y2, (x1 - x2)**2 + (y1 - y2)**2)
            buckets[key].append(((x1, y1), (x2, y2)))
    answer = 0
    for diagonals in buckets.values():
        for i, (p, q) in enumerate(diagonals):
            for r, s in diagonals[i + 1:]:
                area = abs((r[0]-p[0])*(s[1]-p[1]) - (r[1]-p[1])*(s[0]-p[0]))
                answer = max(answer, area)
    return answer


# Faster follow-up: within each bucket, choose diagonals closest to perpendicular.
# Area = |cross(diagonal1, diagonal2)| / 2, greatest near a 90-degree angle.
# O(P^2 log P) time, O(P^2) space. atan2 uses floating-point angle ordering;
# for extremely large/precision-sensitive coordinates use exact angular comparison.
def maximum_rectangle_area_fast(points):
    points = list(set(map(tuple, points)))
    buckets = defaultdict(list)
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            if dy < 0 or (dy == 0 and dx < 0):
                dx, dy = -dx, -dy
            buckets[(x1+x2, y1+y2, dx*dx+dy*dy)].append((atan2(dy, dx), dx, dy))
    twice_area = 0
    for vectors in buckets.values():
        vectors.sort()
        k = len(vectors)
        if k < 2:
            continue
        angles = [angle for angle, _, _ in vectors]
        angles += [angle + pi for angle in angles]
        for i, (angle, dx, dy) in enumerate(vectors):
            j = bisect_left(angles, angle + pi / 2, i + 1, i + k)
            for candidate in (j - 1, j):
                if i < candidate < i + k:
                    _, ex, ey = vectors[candidate % k]
                    twice_area = max(twice_area, abs(dx*ey - dy*ex))
    return twice_area / 2



# 03. Course Scheduling and Dependency Variants
# Kahn's algorithm: repeatedly take a node with no unmet prerequisites.
# Generic edges (u, v) mean u BEFORE v; return None if a cycle exists.
# Time and space O(V+E). Nested grouping needs an agreed grouping rule.
def topological_order(vertices, edges):
    graph = {v: [] for v in vertices}
    indegree = dict.fromkeys(graph, 0)
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue = deque(v for v in graph if indegree[v] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in graph[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return order if len(order) == len(graph) else None


def course_order(n, prerequisites):
    # Input [course, prerequisite] reverses the generic edge convention.
    result = topological_order(range(n), [(pre, course) for course, pre in prerequisites])
    return result if result is not None else []


def can_merge_orders(a, b):
    # Equal values represent the same node; repeated values within a list
    # require clarification if duplicate occurrences are intended as distinct.
    edges = [(row[i], row[i+1]) for row in (a, b) for i in range(len(row)-1)]
    return topological_order(set(a) | set(b), edges) is not None



# 03: exclude broken nodes AND all their downstream dependents, then find a path.
# graph is directed adjacency; includes all vertices. O(V+E) time/space.
def path_without_damaged_nodes(graph, start, target, damaged):
    blocked, queue = set(damaged), deque(damaged)
    while queue:
        node = queue.popleft()
        for child in graph.get(node, []):
            if child not in blocked:
                blocked.add(child)
                queue.append(child)
    if start in blocked or target in blocked:
        return None
    parent, queue = {start: None}, deque([start])
    while queue:
        node = queue.popleft()
        if node == target:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for child in graph.get(node, []):
            if child not in blocked and child not in parent:
                parent[child] = node
                queue.append(child)
    return None



# 03: a separate rule: damaged nodes ARE traversable but cost 1; others cost 0.
# Include the starting node's damage. 0–1 BFS minimizes damaged nodes visited.
# O(V+E) time/space. This does NOT remove downstream nodes.
def minimum_damaged_on_path(graph, start, target, damaged):
    damaged = set(damaged)
    best = {start: int(start in damaged)}
    queue = deque([(start, best[start])])
    while queue:
        node, cost = queue.popleft()
        if cost != best[node]:
            continue
        if node == target:
            return cost
        for child in graph.get(node, []):
            weight = int(child in damaged)
            score = cost + weight
            if score < best.get(child, inf):
                best[child] = score
                if weight:
                    queue.append((child, score))
                else:
                    queue.appendleft((child, score))
    return -1



# 03: independent topological-order checker. O(V+E).
def valid_topological_order(vertices, edges, order):
    vertices = set(vertices)
    if len(order) != len(vertices) or set(order) != vertices:
        return False
    position = {node: i for i, node in enumerate(order)}
    return all(position[u] < position[v] for u, v in edges)



# 04. Connected Crop Arrangement on a Grid
# counts[i] cells receive crop i+1; counts must sum to rows*cols.
# A consecutive segment of a snake path is always 4-connected.
# Time O(rows*cols + K); space O(rows*cols), including output.
def arrange_crops(rows, cols, counts):
    if any(count < 0 for count in counts) or sum(counts) != rows * cols:
        raise ValueError("Invalid crop counts")
    crops = (crop for crop, count in enumerate(counts, 1) for _ in range(count))
    grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        columns = range(cols) if r % 2 == 0 else range(cols-1, -1, -1)
        for c in columns:
            grid[r][c] = next(crops)
    return grid


# Follow-up: squares n*n and m*m, side by side with TOP edges aligned.
# Other placements/offsets need their own path construction.
def arrange_two_gardens(n, m, counts):
    if n < 1 or m < 1 or any(x < 0 for x in counts) or sum(counts) != n*n + m*m:
        raise ValueError("Invalid garden sizes or counts")
    path = []
    for c in range(n):
        downward = (c % 2 == 0) == (n % 2 == 0)
        rows = range(n) if downward else range(n-1, -1, -1)
        path.extend((r, c) for r in rows)
    for r in range(m):
        columns = range(n, n+m) if r % 2 == 0 else range(n+m-1, n-1, -1)
        path.extend((r, c) for c in columns)
    crops = (crop for crop, count in enumerate(counts, 1) for _ in range(count))
    return {cell: crop for cell, crop in zip(path, crops)}



# 05. Longest Non-Decreasing Subarray with One Replacement
# At most one element may become ANY value; non-strict <= comparisons.
# left/right run lengths allow each replacement to be evaluated in O(1).
# Time O(N), space O(N). strict=True assumes replacement is an INTEGER.
def longest_with_one_change(values, strict=False):
    n = len(values)
    if n <= 2:
        return n
    left, right = [1]*n, [1]*n
    def ordered(a, b):
        return a < b if strict else a <= b
    for i in range(1, n):
        if ordered(values[i-1], values[i]):
            left[i] = left[i-1]+1
    for i in range(n-2, -1, -1):
        if ordered(values[i], values[i+1]):
            right[i] = right[i+1]+1
    best = max(left)
    for i in range(n):
        before = left[i-1] if i else 0
        after = right[i+1] if i+1 < n else 0
        best = max(best, before+1, after+1)
        if 0 < i < n-1:
            can_bridge = (values[i+1]-values[i-1] >= 2 if strict
                          else values[i-1] <= values[i+1])
            if can_bridge:
                best = max(best, before+1+after)
    return best



# 06. Number of Islands
# '1' is land, '0' water; four directions. Mutates the grid to mark visited.
# Time O(R*C); auxiliary space O(R*C) worst case. Accepts list-of-list grids.
def number_of_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols, answer = len(grid), len(grid[0]), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            answer += 1
            grid[r][c] = "0"
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in DIRECTIONS:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"
                        stack.append((nx, ny))
    return answer


# Follow-up: land arrives one cell at a time. Duplicate additions change nothing.
# Each insertion O(alpha(R*C)) amortized; O(R*C) memory.
class IslandCounter:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.uf, self.land, self.count = UnionFind(rows*cols), set(), 0

    def add(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise ValueError("Cell outside grid")
        if (r, c) in self.land:
            return self.count
        self.land.add((r, c))
        self.count += 1
        for dr, dc in DIRECTIONS:
            nr, nc = r+dr, c+dc
            if (nr, nc) in self.land and self.uf.union(r*self.cols+c, nr*self.cols+nc):
                self.count -= 1
        return self.count



# 06: largest island area; numeric 1/0 grid, does not mutate it.
def largest_island_area(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols, seen, answer = len(grid), len(grid[0]), set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or (r,c) in seen:
                continue
            seen.add((r,c))
            stack, area = [(r,c)], 0
            while stack:
                x,y = stack.pop()
                area += 1
                for dx,dy in DIRECTIONS:
                    nx,ny = x+dx,y+dy
                    if (0 <= nx < rows and 0 <= ny < cols
                            and grid[nx][ny] == 1 and (nx,ny) not in seen):
                        seen.add((nx,ny))
                        stack.append((nx,ny))
            answer = max(answer, area)
    return answer



# 06: huge grid arrives row by row (strings of '0'/'1'). Keep only row labels.
# An island is finished once none of its labels survives into the next row.
# O(R*C*alpha(C)) time, O(C) auxiliary memory; rows must have equal width.
def count_islands_stream(row_stream):
    previous, finished = [], 0
    for row in row_stream:
        if previous and len(row) != len(previous):
            raise ValueError("Rows must have equal width")
        old_count = max(previous, default=-1) + 1
        uf = UnionFind(old_count + len(row))
        current = [-1]*len(row)
        for c, cell in enumerate(row):
            if cell != "1":
                continue
            label = old_count+c
            current[c] = label
            if c and current[c-1] != -1:
                uf.union(label, current[c-1])
            if previous and previous[c] != -1:
                uf.union(label, previous[c])
        old_roots = {uf.find(label) for label in previous if label != -1}
        new_roots = {uf.find(label) for label in current if label != -1}
        finished += len(old_roots - new_roots)
        compact = {root:i for i,root in enumerate(new_roots)}
        previous = [compact[uf.find(label)] if label != -1 else -1 for label in current]
    return finished + len({label for label in previous if label != -1})



# 06: ONLINE add/remove: straightforward working fallback, NOT optimal dynamic DSU.
# Rebuild count after each edit, O(R*C) per operation. Union-Find alone cannot split.
# For faster known-in-advance deletions, use offline rollback connectivity (Q01).
def island_counts_with_removals(rows, cols, operations):
    grid, result = [["0"]*cols for _ in range(rows)], []
    for action, r, c in operations:
        if action not in ("add", "remove"):
            raise ValueError("Unknown action")
        grid[r][c] = "1" if action == "add" else "0"
        result.append(number_of_islands([row[:] for row in grid]))
    return result



# 07. Path Minimizing the Maximum Cell (Swim in Rising Water)
# Dijkstra with max(current_score, neighbor_height), not addition.
# Optional endpoints; empty grid returns 0. Time O(R*C log(R*C)), space O(R*C).
def minimum_path_threshold(grid, start=(0, 0), target=None):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    target = target if target is not None else (rows-1, cols-1)
    r, c = start
    best = {start: grid[r][c]}
    heap = [(grid[r][c], r, c)]
    while heap:
        score, r, c = heappop(heap)
        if score != best[(r, c)]:
            continue
        if (r, c) == target:
            return score
        for dr, dc in DIRECTIONS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_score = max(score, grid[nr][nc])
                if new_score < best.get((nr, nc), inf):
                    best[(nr, nc)] = new_score
                    heappush(heap, (new_score, nr, nc))
    return -1


# Safety variant: adjacency {node: [(neighbor, edge_safety), ...]}.
# Inclusive threshold by default; undirected input must contain both directions.
# Assumes nonnegative safety values. O((V+E) log(V+E)) time, O(V+E) space.
def minimum_graph_threshold(graph, start, target, limit, inclusive=True):
    best, heap = {start: 0}, [(0, start)]
    while heap:
        cost, node = heappop(heap)
        if cost != best[node]:
            continue
        if node == target:
            return cost
        for neighbor, weight in graph.get(node, []):
            if weight > limit or (not inclusive and weight == limit):
                continue
            score = max(cost, weight)
            if score < best.get(neighbor, inf):
                best[neighbor] = score
                heappush(heap, (score, neighbor))
    return -1


# Cat variant: grid uses 1=land, 0=water; cat distance is Manhattan, ignoring water.
# Maximize the MINIMUM distance to cat along the route (max-heap via negative scores).
def safest_path_score(grid, start, target, cat):
    rows, cols = len(grid), len(grid[0])
    if not grid[start[0]][start[1]] or not grid[target[0]][target[1]]:
        return -1
    def distance(r, c):
        return abs(r-cat[0]) + abs(c-cat[1])
    best = {start: distance(*start)}
    heap = [(-best[start], *start)]
    while heap:
        negative_score, r, c = heappop(heap)
        score = -negative_score
        if score != best[(r, c)]:
            continue
        if (r, c) == target:
            return score
        for dr, dc in DIRECTIONS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                new_score = min(score, distance(nr, nc))
                if new_score > best.get((nr, nc), -1):
                    best[(nr, nc)] = new_score
                    heappush(heap, (-new_score, nr, nc))
    return -1


# Network delay follow-up: directed edges (u,v,weight), nodes 1..n; nonnegative weights.
# Add weights; return largest shortest distance, -1 if someone is unreachable.
def network_delay(n, edges, source):
    graph = defaultdict(list)
    for u, v, weight in edges:
        graph[u].append((v, weight))
    best, heap = {source: 0}, [(0, source)]
    while heap:
        cost, node = heappop(heap)
        if cost != best[node]:
            continue
        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < best.get(neighbor, inf):
                best[neighbor] = new_cost
                heappush(heap, (new_cost, neighbor))
    return max(best.values()) if len(best) == n else -1



# 08. Shortest Path Nodes and Escaping a Pursuer
# Unweighted UNDIRECTED adjacency lists/dict. Return (length, on-path nodes, safe).
# Missing route: (None, set(), False). Bob may wait; ties mean caught at a node.
# Alice must follow a shortest path; both move one edge per tick.
# Three BFS runs + traversal of shortest-path layers: O(V+E) time, O(V) extra space.
def shortest_path_info(graph, alice, target, bob):
    def bfs(source):
        distance, queue = {source: 0}, deque([source])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distance:
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        return distance
    da, dt, db = bfs(alice), bfs(target), bfs(bob)
    if target not in da:
        return None, set(), False
    length = da[target]
    on_path = {v for v in da if v in dt and da[v] + dt[v] == length}
    seen = {alice} if db.get(alice, inf) > 0 else set()
    queue = deque(seen)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if (neighbor in on_path and neighbor not in seen
                    and da[neighbor] == da[node]+1
                    and da[neighbor] < db.get(neighbor, inf)):
                seen.add(neighbor)
                queue.append(neighbor)
    return length, on_path, target in seen



# 09. Meeting Rooms / Interval Scheduling Variants
# Half-open [start,end): ending at t and starting at t do not overlap.
# Positive-length intervals; sweep ends before starts at ties.
# O(M log M) time, O(M) space.
def min_meeting_rooms(intervals):
    events = [(start, 1) for start, end in intervals if start < end]
    events += [(end, -1) for start, end in intervals if start < end]
    active = answer = 0
    for time, change in sorted(events):
        active += change
        answer = max(answer, active)
    return answer


# Assignment follow-up: output one zero-based room ID per original input interval.
# The earliest-ending room is reused; total room count is minimal.
def assign_rooms(intervals):
    heap, assignment, rooms = [], [None]*len(intervals), 0
    for i, (start, end) in sorted(enumerate(intervals), key=lambda item: item[1][0]):
        if start >= end:
            raise ValueError("Assignment expects positive-length intervals")
        if heap and heap[0][0] <= start:
            _, room = heappop(heap)
        else:
            room = rooms
            rooms += 1
        assignment[i] = room
        heappush(heap, (end, room))
    return assignment, rooms


# Cyclic daily intervals: 0 <= start,end < day; start > end wraps midnight.
# Equal endpoints mean an empty interval (a full-day booking needs a separate rule).
def min_rooms_cyclic(intervals, day=1440):
    pieces = []
    for start, end in intervals:
        if start < end:
            pieces.append((start, end))
        elif start > end:
            pieces.extend(((start, day), (0, end)))
    return min_meeting_rooms(pieces)


# Exactly-X concurrency follow-up, merging adjacent qualifying segments.
def exact_concurrency_ranges(intervals, wanted):
    changes = Counter()
    for start, end in intervals:
        if start < end:
            changes[start] += 1
            changes[end] -= 1
    active, result, previous = 0, [], None
    for time in sorted(changes):
        if previous is not None and previous < time and active == wanted:
            if result and result[-1][1] == previous:
                result[-1] = (result[-1][0], time)
            else:
                result.append((previous, time))
        active += changes[time]
        previous = time
    return result


# On-call sets: records (name,start,end), repeated records for a name count once
# in the active set; return (start,end,frozenset(names)), omit gaps.
# Sorting O(M log M); copying output sets costs the total number of emitted names.
def on_call_segments(records):
    changes = defaultdict(list)
    for name, start, end in records:
        if start < end:
            changes[start].append((name, 1))
            changes[end].append((name, -1))
    active, result, previous = Counter(), [], None
    for time in sorted(changes):
        if previous is not None and previous < time and active:
            names = frozenset(active)
            if result and result[-1][1] == previous and result[-1][2] == names:
                result[-1] = (result[-1][0], time, names)
            else:
                result.append((previous, time, names))
        for name, delta in changes[time]:
            active[name] += delta
            if not active[name]:
                del active[name]
        previous = time
    return result


# Maximum-profit scheduling variant (LC1235): jobs=(start,end,profit).
# Binary search + DP: O(M log M) time, O(M) space.
def maximum_job_profit(jobs):
    jobs = sorted(jobs, key=lambda job: job[1])
    ends, best = [end for start, end, profit in jobs], [0]
    for i, (start, end, profit) in enumerate(jobs):
        previous_count = bisect_right(ends, start, 0, i)
        best.append(max(best[-1], best[previous_count] + profit))
    return best[-1]



# 09: overlap of two half-open intervals; zero-length intervals do not overlap.
def intervals_overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])



# 09: car rentals (reservation_id,pickup,return). Reuse room assignment.
# Optional capacity: return None if this fleet cannot serve all reservations.
def assign_rentals(reservations, capacity=None):
    assignments, fleet = assign_rooms([(start,end) for _,start,end in reservations])
    if capacity is not None and fleet > capacity:
        return None
    return {reservation[0]:car for reservation,car in zip(reservations,assignments)}, fleet



# 09: every attendee free within a specified [day_start,day_end) horizon.
# calendars is a list of attendee interval lists; complement the combined busy union.
def common_free_time(calendars, day_start, day_end):
    busy = sorted((max(start,day_start), min(end,day_end))
                  for calendar in calendars for start,end in calendar
                  if start < end and start < day_end and end > day_start)
    result, cursor = [], day_start
    for start,end in busy:
        if start > cursor:
            result.append((cursor,start))
        cursor = max(cursor,end)
    if cursor < day_end:
        result.append((cursor,day_end))
    return result



# 09: merge already sorted shard timelines (time,delta) without loading them all.
# O(E log S) time, O(S) memory for S streams. Aggregate same-time changes together.
def min_rooms_from_shards(shards):
    from heapq import merge
    active = answer = 0
    previous, change = None, 0
    for time, delta in merge(*shards):
        if previous is not None and time != previous:
            active += change
            answer = max(answer,active)
            change = 0
        previous = time
        change += delta
    return max(answer,active+change)



# 09: one-person gate per tick, action='enter'/'exit'; original index breaks ties.
# Prior tick's direction wins; idle defaults to exit. Input may be unsorted.
# O(N log N) with sorting, O(N) if arrivals already ordered; O(N) space.
def gate_crossing_times(events):
    arrivals = sorted(enumerate(events), key=lambda item: (item[1][0],item[0]))
    queues, answers, i, time, direction = [deque(),deque()], [0]*len(events), 0, 0, 1
    while i < len(arrivals) or queues[0] or queues[1]:
        if not queues[0] and not queues[1] and time < arrivals[i][1][0]:
            time = arrivals[i][1][0]
            direction = 1
        while i < len(arrivals) and arrivals[i][1][0] <= time:
            person, (_,action) = arrivals[i]
            if action not in ("enter","exit"):
                raise ValueError("Unknown gate action")
            queues[action == "exit"].append(person)
            i += 1
        if not queues[direction]:
            direction = 1-direction
        answers[queues[direction].popleft()] = time
        time += 1
    return answers



# 10. Range Duplicate Check with Constant-Time Queries
# Inclusive [left,right]; latest valid start for a unique suffix ending at right.
# O(N) preprocessing/update, O(1) query, O(N) space; hashable values.
class RangeUnique:
    def __init__(self, values):
        self.values = list(values)
        self._build()

    def _build(self):
        last, start = {}, 0
        self.start = []
        for i, value in enumerate(self.values):
            start = max(start, last.get(value, -1) + 1)
            self.start.append(start)
            last[value] = i

    def unique(self, left, right):
        if not 0 <= left <= right < len(self.values):
            raise ValueError("Invalid inclusive range")
        return left >= self.start[right]

    def update(self, index, value):
        self.values[index] = value
        self._build()



# 11. Grid Path Count with Diagonal Moves and Checkpoints
# Start bottom-left, finish bottom-right. Every move advances ONE column:
# up-right / right / down-right. Checkpoints are (row,col).
# A path visits every checkpoint; ordered=True preserves their supplied order.
# Identical duplicate checkpoints are treated as one requirement.
# Time O(R*C+K), space O(R+K). Integer counts may become very large.
def count_grid_paths(rows, cols, checkpoints=(), ordered=False):
    if rows <= 0 or cols <= 0:
        return 0
    required, previous_col = {}, -1
    for r, c in checkpoints:
        if not (0 <= r < rows and 0 <= c < cols):
            return 0
        if c in required and required[c] != r:
            return 0
        if ordered and c < previous_col:
            return 0
        required[c], previous_col = r, c
    ways = [0]*rows
    ways[rows-1] = 1
    for c in range(cols):
        if c:
            next_ways = [0]*rows
            for r in range(rows):
                next_ways[r] = ways[r]
                if r:
                    next_ways[r] += ways[r-1]
                if r+1 < rows:
                    next_ways[r] += ways[r+1]
            ways = next_ways
        if c in required:
            for r in range(rows):
                if r != required[c]:
                    ways[r] = 0
    return ways[rows-1]



# 12. URL Request Handler Router
# Segment trie: {id} matches exactly one nonempty path segment.
# Literal wins at the first differing segment, but may fail later: BACKTRACK.
# Ignore leading/trailing slashes; no query-string/decoding normalization.
# Duplicate structural route: first registration wins. Returns registered pattern.
# Build O(total segments); lookup O(visited trie nodes + path length),
# possibly O(total trie size), not guaranteed O(path length) with wildcards.
class RouteNode:
    def __init__(self):
        self.literal, self.wildcard, self.handler = {}, None, None


class Router:
    def __init__(self, patterns=()):
        self.root = RouteNode()
        for pattern in patterns:
            self.add(pattern)

    def add(self, pattern):
        node = self.root
        for segment in pattern.strip("/").split("/") if pattern.strip("/") else []:
            if segment.startswith("{") and segment.endswith("}"):
                if node.wildcard is None:
                    node.wildcard = RouteNode()
                node = node.wildcard
            else:
                if segment not in node.literal:
                    node.literal[segment] = RouteNode()
                node = node.literal[segment]
        if node.handler is None:
            node.handler = pattern

    def match(self, path):
        segments = path.strip("/").split("/") if path.strip("/") else []
        stack = [(self.root, 0)]
        while stack:
            node, i = stack.pop()
            if i == len(segments):
                if node.handler is not None:
                    return node.handler
                continue
            # Wildcard goes in FIRST so the literal branch comes out FIRST.
            if node.wildcard is not None and segments[i]:
                stack.append((node.wildcard, i+1))
            if segments[i] in node.literal:
                stack.append((node.literal[segments[i]], i+1))
        return None



# 12: return captured parameter names from the MATCHED stored pattern.
# Names must be distinct within one pattern; returns None or (pattern,parameters).
def route_with_parameters(router,path):
    pattern = router.match(path)
    if pattern is None:
        return None
    parameters = {}
    for segment,value in zip(pattern.strip("/").split("/"),path.strip("/").split("/")):
        if segment.startswith("{") and segment.endswith("}"):
            parameters[segment[1:-1]] = value
    return pattern,parameters


class MethodRouter:
    def __init__(self):
        self.routers = {}

    def add(self,method,pattern):
        if method not in self.routers:
            self.routers[method] = Router()
        self.routers[method].add(pattern)

    def match(self,method,path):
        return self.routers[method].match(path) if method in self.routers else None



# 12: terminal '*' matches zero or more remaining segments.
# Precedence at each branch: literal, then {parameter}, then '*'.
class RestRouter(Router):
    def add(self,pattern):
        if not pattern.endswith("/*"):
            return super().add(pattern)
        node = self.root
        for segment in pattern[:-2].strip("/").split("/") if pattern[:-2].strip("/") else []:
            if segment.startswith("{") and segment.endswith("}"):
                if node.wildcard is None:
                    node.wildcard = RouteNode()
                node = node.wildcard
            else:
                if segment not in node.literal:
                    node.literal[segment] = RouteNode()
                node = node.literal[segment]
        if not hasattr(node,"rest"):
            node.rest = pattern

    def match(self,path):
        segments = path.strip("/").split("/") if path.strip("/") else []
        # Stack items: trie node, next segment index, fallback pattern (or None).
        stack = [(self.root,0,None)]
        while stack:
            node,i,fallback = stack.pop()
            if fallback is not None:
                return fallback
            if i == len(segments):
                if node.handler is not None:
                    return node.handler
                if hasattr(node,"rest"):
                    return node.rest
                continue
            if hasattr(node,"rest"):
                stack.append((node,i,node.rest))
            if node.wildcard is not None and segments[i]:
                stack.append((node.wildcard,i+1,None))
            if segments[i] in node.literal:
                stack.append((node.literal[segments[i]],i+1,None))
        return None



# 13. Expression Tree Single-Leaf Mutation
# BoolNode: leaves val=True/False; binary AND/OR/XOR, unary NOT uses left.
# Return root results for each INDEPENDENT leaf flip, in left-to-right order.
# Faster than recomputing every ancestor: propagate whether a flip can matter.
# An AND child matters iff its sibling is True; OR iff sibling is False;
# XOR and NOT always pass a change upward. Ancestors must also be sensitive.
# Time O(N), space O(N). Original tree is never mutated.
class BoolNode:
    def __init__(self, op=None, left=None, right=None, val=None):
        self.op, self.left, self.right, self.val = op, left, right, val


def leaf_flip_results(root):
    if root is None:
        return []
    values, stack = {}, [(root, False)]
    while stack:
        node, ready = stack.pop()
        if node.op is None:
            values[node] = bool(node.val)
        elif not ready:
            stack.append((node, True))
            if node.op != "NOT":
                stack.append((node.right, False))
            stack.append((node.left, False))
        else:
            a = values[node.left]
            if node.op == "NOT":
                values[node] = not a
            elif node.op == "AND":
                values[node] = a and values[node.right]
            elif node.op == "OR":
                values[node] = a or values[node.right]
            elif node.op == "XOR":
                values[node] = a != values[node.right]
            else:
                raise ValueError("Unknown boolean operator")
    result, stack = [], [(root, True)]
    while stack:
        node, sensitive = stack.pop()
        if node.op is None:
            result.append(values[root] != sensitive)
        elif node.op == "NOT":
            stack.append((node.left, sensitive))
        else:
            left_sensitive = right_sensitive = sensitive
            if node.op == "AND":
                left_sensitive = sensitive and values[node.right]
                right_sensitive = sensitive and values[node.left]
            elif node.op == "OR":
                left_sensitive = sensitive and not values[node.right]
                right_sensitive = sensitive and not values[node.left]
            stack.append((node.right, right_sensitive))
            stack.append((node.left, left_sensitive))
    return result



# 13: persistent leaf flips / batches, using cached values and parent links.
# O(N) build/space; O(height) per flip, early stop if a parent's value stays the same.
class BooleanExpression:
    def __init__(self, root):
        self.root, self.parent, self.values = root, {}, {}
        stack = [(root,None,False)]
        while stack:
            node,parent,ready = stack.pop()
            self.parent[node] = parent
            if node.op is None:
                self.values[node] = bool(node.val)
            elif not ready:
                stack.append((node,parent,True))
                if node.op != "NOT":
                    stack.append((node.right,node,False))
                stack.append((node.left,node,False))
            else:
                self.values[node] = self._value(node)

    def _value(self,node):
        a = self.values[node.left]
        if node.op == "NOT":
            return not a
        b = self.values[node.right]
        if node.op == "AND":
            return a and b
        if node.op == "OR":
            return a or b
        if node.op == "XOR":
            return a != b
        raise ValueError("Unknown operator")

    def flip(self,leaf):
        if leaf not in self.values or leaf.op is not None:
            raise ValueError("Expected a leaf of this expression")
        self.values[leaf] = not self.values[leaf]
        node = self.parent[leaf]
        while node is not None:
            new = self._value(node)
            if new == self.values[node]:
                break
            self.values[node] = new
            node = self.parent[node]
        return self.values[self.root]

    def flip_many(self,leaves):
        for leaf in leaves:
            self.flip(leaf)
        return self.values[self.root]

    def sensitive_leaves(self):
        # Uses CURRENT values after persistent flips.
        result, stack = [], [(self.root,True)]
        while stack:
            node,matters = stack.pop()
            if not matters:
                continue
            if node.op is None:
                result.append(node)
            elif node.op == "NOT":
                stack.append((node.left,True))
            else:
                left = right = True
                if node.op == "AND":
                    left,right = self.values[node.right],self.values[node.left]
                elif node.op == "OR":
                    left,right = not self.values[node.right],not self.values[node.left]
                stack.extend(((node.right,right),(node.left,left)))
        return result



# 14. Active Communication Top Users
# Undirected distinct pairs, duplicates ignored. Self pairs ignored by default.
# top_k breaks ties alphabetically; most_active_user allows ANY tied maximum.
# O(1) expected per pair and most-active lookup, O(U log(k+1)) top_k;
# space O(E+U), potentially O(U^2) for the edge set.
class ActiveCommunication:
    def __init__(self, count_self=False):
        self.edges, self.counts = set(), Counter()
        self.winner, self.count_self = None, count_self

    def add(self, pair):
        a, b = pair.split("-") if isinstance(pair, str) else pair
        edge = tuple(sorted((a, b)))
        if edge in self.edges or (a == b and not self.count_self):
            return
        self.edges.add(edge)
        for user in set((a, b)):
            self.counts[user] += 1
            if self.winner is None or self.counts[user] > self.counts[self.winner]:
                self.winner = user

    register = add

    def most_active_user(self):
        return self.winner

    def top_k(self, k):
        return nsmallest(max(0, k), self.counts, key=lambda user: (-self.counts[user], user))



# 15. Temperature Monitoring Data Structure
# Last N READINGS, average over readings received so far; empty queries return None.
# Running sum + decreasing deque. O(1) amortized insert; O(1) average/max;
# O(N) space. A single insert can discard O(N) smaller maximum candidates.
class TemperatureMonitor:
    def __init__(self, n):
        if n < 1:
            raise ValueError("Window size must be positive")
        self.n, self.window, self.maxima = n, deque(), deque()
        self.total, self.index = 0, 0

    def insert(self, value):
        self.window.append(value)
        self.total += value
        if len(self.window) > self.n:
            self.total -= self.window.popleft()
        while self.maxima and self.maxima[-1][1] <= value:
            self.maxima.pop()
        self.maxima.append((self.index, value))
        while self.maxima[0][0] <= self.index-self.n:
            self.maxima.popleft()
        self.index += 1

    def average(self):
        return self.total / len(self.window) if self.window else None

    def maximum(self):
        return self.maxima[0][1] if self.maxima else None


# Time-window variant: chronological timestamps; keep readings in (now-span, now].
# Queries optionally expire stale readings even when no new readings arrive.
class TimeTemperatureMonitor:
    def __init__(self, span):
        if span <= 0:
            raise ValueError("Span must be positive")
        self.span, self.window, self.maxima = span, deque(), deque()
        self.total, self.clock = 0, -inf

    def _expire(self, now):
        if now < self.clock:
            raise ValueError("Time must not move backwards")
        self.clock = now
        while self.window and self.window[0][0] <= now-self.span:
            self.total -= self.window.popleft()[1]
        while self.maxima and self.maxima[0][0] <= now-self.span:
            self.maxima.popleft()

    def insert(self, time, value):
        self._expire(time)
        self.window.append((time, value))
        self.total += value
        while self.maxima and self.maxima[-1][1] <= value:
            self.maxima.pop()
        self.maxima.append((time, value))

    def average(self, now=None):
        if now is not None:
            self._expire(now)
        return self.total / len(self.window) if self.window else None

    def maximum(self, now=None):
        if now is not None:
            self._expire(now)
        return self.maxima[0][1] if self.maxima else None



# 15: minimum uses a second monotonic deque; inherits sum/maximum code.
class TemperatureMinMonitor(TemperatureMonitor):
    def __init__(self,n):
        super().__init__(n)
        self.minima = deque()

    def insert(self,value):
        index = self.index
        super().insert(value)
        while self.minima and self.minima[-1][1] >= value:
            self.minima.pop()
        self.minima.append((index,value))
        while self.minima[0][0] <= index-self.n:
            self.minima.popleft()

    def minimum(self):
        return self.minima[0][1] if self.minima else None



# 15: median of last N readings: two heaps, lazy expiration, periodic compaction.
# O(log N) amortized insertion, O(1) median query after insertion, O(N) memory.
# Larger lower-half heap stores negatives; each reading has a unique index.
class SlidingMedian:
    def __init__(self,n):
        if n < 1:
            raise ValueError("Window must be positive")
        self.n, self.low, self.high, self.window = n, [], [], deque()
        self.side, self.dead, self.index = {}, set(), 0
        self.low_size = self.high_size = 0

    def _prune(self,heap):
        while heap and heap[0][1] in self.dead:
            _,index = heappop(heap)
            self.dead.remove(index)

    def _balance(self):
        self._prune(self.low)
        self._prune(self.high)
        while self.low_size > self.high_size+1:
            value,index = heappop(self.low)
            heappush(self.high,(-value,index))
            self.side[index] = "high"
            self.low_size -= 1
            self.high_size += 1
            self._prune(self.low)
        while self.low_size < self.high_size:
            value,index = heappop(self.high)
            heappush(self.low,(-value,index))
            self.side[index] = "low"
            self.high_size -= 1
            self.low_size += 1
            self._prune(self.high)

    def insert(self,value):
        index = self.index
        self.index += 1
        self.window.append((value,index))
        if not self.low or value <= -self.low[0][0]:
            heappush(self.low,(-value,index))
            self.side[index] = "low"
            self.low_size += 1
        else:
            heappush(self.high,(value,index))
            self.side[index] = "high"
            self.high_size += 1
        if len(self.window) > self.n:
            _,old = self.window.popleft()
            self.dead.add(old)
            if self.side.pop(old) == "low":
                self.low_size -= 1
            else:
                self.high_size -= 1
        self._balance()
        # Lazy entries buried in a heap must not accumulate without bound.
        if len(self.low)+len(self.high) > 4*self.n:
            from heapq import heapify
            self.low = [(-v,i) for v,i in self.window if self.side[i] == "low"]
            self.high = [(v,i) for v,i in self.window if self.side[i] == "high"]
            heapify(self.low)
            heapify(self.high)
            self.dead.clear()

    def median(self):
        if not self.window:
            return None
        if self.low_size > self.high_size:
            return -self.low[0][0]
        return (-self.low[0][0]+self.high[0][0])/2



# 16. Robot Status Message Deduplication Window
# Chronological stream; allow exactly window seconds after LAST DISPLAY.
# Hidden arrivals do not change the saved time. O(1) expected/event; O(U) space.
# Out-of-order events need an agreed policy; rejecting them avoids silently
# pretending this chronological algorithm handles unspecified historical rules.
class MessageDeduplicator:
    def __init__(self, window=10):
        self.window, self.last_displayed, self.clock = window, {}, -inf

    def should_print(self, time, message):
        if time < self.clock:
            raise ValueError("Chronological timestamps required")
        self.clock = time
        if message in self.last_displayed and time-self.last_displayed[message] < self.window:
            return False
        self.last_displayed[message] = time
        return True



# 16: one explicit OUT-OF-ORDER policy: never revise earlier display decisions;
# accept a late event only if it is at least window seconds from every display
# of the same message, in either direction. Nearest neighbors suffice.
# Sorted-list version: O(log M) search but O(M) insertion; O(M) stored history.
# A balanced ordered set gives O(log M) insertion if the interview permits one.
class OutOfOrderMessageDeduplicator:
    def __init__(self,window=10):
        self.window, self.history = window, defaultdict(list)

    def should_print(self,time,message):
        times = self.history[message]
        i = bisect_left(times,time)
        if i and time-times[i-1] < self.window:
            return False
        if i < len(times) and times[i]-time < self.window:
            return False
        times.insert(i,time)
        return True



# Interview-style direct assertions: normal, boundary, and tricky examples.
def run_examples():
    events = [(1, 0, 1, "friend"), (5, 1, 2, "friend")]
    assert friendship_group_counts(3, events) == [(1,2),(5,1)]
    assert earliest_all_connected(3, events) == 5
    assert earliest_all_connected(3, events[:1]) == -1
    assert connected_at_times(3, events, [(0, 0, 2), (5, 0, 2)]) == [False, True]
    assert earliest_connected_with_unfriend(3, events[:1] + [(2,0,1,"unfriend"),
        (3,1,2,"friend"), (4,0,1,"friend")]) == 4
    points = [(0,0), (2,0), (2,1), (0,1)]
    assert maximum_rectangle_area(points) == 2
    assert maximum_rectangle_area_fast(points) == 2
    assert maximum_rectangle_area([(0,0), (1,1), (2,0), (1,-1)]) == 2
    assert course_order(3, [(1,0), (2,1)]) == [0,1,2]
    assert course_order(2, [(1,0), (0,1)]) == []
    assert can_merge_orders([1,2,3], [2,4,5])
    assert not can_merge_orders([1,6,4], [4,1])
    assert arrange_crops(2,3,[3,3]) == [[1,1,1], [2,2,2]]
    assert len(arrange_two_gardens(2,3,[4,9])) == 13
    assert number_of_islands([list("110"),list("001")]) == 2
    islands = IslandCounter(2,2)
    assert [islands.add(*cell) for cell in [(0,0),(1,1),(0,1),(0,1)]] == [1,2,1,1]
    assert minimum_path_threshold([[0,2],[1,3]]) == 3
    assert minimum_graph_threshold({0:[(1,4)],1:[(2,2)],2:[]},0,2,4) == 4
    assert minimum_graph_threshold({0:[(1,4)]},0,1,4,inclusive=False) == -1
    assert safest_path_score([[1,1],[1,1]], (0,0), (0,1), (1,1)) == 1
    assert network_delay(3, [(1,2,2),(2,3,1)], 1) == 3
    graph = {0:[1],1:[0,2],2:[1],3:[]}
    assert shortest_path_info(graph,0,2,3) == (2,{0,1,2},True)
    assert shortest_path_info(graph,0,2,2) == (2,{0,1,2},False)
    assert min_meeting_rooms([(0,30),(5,10),(15,20)]) == 2
    assert min_meeting_rooms([(0,1),(1,2)]) == 1
    assert assign_rooms([(0,30),(5,10),(15,20)])[1] == 2
    assert min_rooms_cyclic([(23,2),(1,3)],day=24) == 2
    assert exact_concurrency_ranges([(0,3),(1,2)],2) == [(1,2)]
    assert on_call_segments([("A",1,3),("B",2,4)]) == [
        (1,2,frozenset("A")),(2,3,frozenset("AB")),(3,4,frozenset("B"))]
    assert maximum_job_profit([(1,3,50),(2,4,10),(3,5,40)]) == 90
    ranges = RangeUnique([1,2,1,3])
    assert ranges.unique(1,3) and not ranges.unique(0,2)
    ranges.update(2,4)
    assert ranges.unique(0,3)
    active = ActiveCommunication()
    for pair in ["A-B","B-A","B-C","A-A"]:
        active.add(pair)
    assert active.most_active_user() == "B"
    assert active.top_k(3) == ["B","A","C"]
    assert longest_with_one_change([1,0,3,4,5,2,3]) == 5
    assert longest_with_one_change([]) == 0
    assert longest_with_one_change([1,1,1],strict=True) == 2
    assert count_grid_paths(2,3) == 2
    assert count_grid_paths(2,3,[(0,1)]) == 1
    assert count_grid_paths(2,3,[(0,1),(1,1)]) == 0
    assert count_grid_paths(1,1,[(0,0)]) == 1
    root = BoolNode("OR", BoolNode(val=True), BoolNode(val=False))
    assert leaf_flip_results(root) == [False,True]
    assert leaf_flip_results(BoolNode("NOT",BoolNode(val=True))) == [True]
    monitor = TemperatureMonitor(2)
    assert monitor.average() is None
    for value in [5,5,1]:
        monitor.insert(value)
    assert monitor.average() == 3 and monitor.maximum() == 5
    monitor.insert(-1)
    assert monitor.average() == 0 and monitor.maximum() == 1
    timed = TimeTemperatureMonitor(10)
    timed.insert(0,8)
    timed.insert(9,2)
    assert timed.average(10) == 2
    assert timed.maximum(19) is None
    router = Router(["/users/{id}/photo", "/users/me/settings"])
    assert router.match("/users/123/photo") == "/users/{id}/photo"
    assert router.match("/users/me/photo") == "/users/{id}/photo"
    assert router.match("/users/me/settings") == "/users/me/settings"
    assert router.match("/users/me/unknown") is None
    logger = MessageDeduplicator()
    assert logger.should_print(10,"solar")
    assert not logger.should_print(13,"solar")
    assert logger.should_print(20,"solar")
    print("All 16 question sections: examples passed.")






def run_followup_examples():
    graph = {0:[1,2],1:[3],2:[3],3:[]}
    assert path_without_damaged_nodes(graph,0,2,{1}) == [0,2]
    assert path_without_damaged_nodes(graph,0,3,{1}) is None
    assert minimum_damaged_on_path(graph,0,3,{1}) == 0
    assert valid_topological_order(range(3),[(0,1),(1,2)],[0,1,2])
    assert largest_island_area([[1,1,0],[0,1,1]]) == 4
    assert count_islands_stream(iter(["110","001"])) == 2
    assert island_counts_with_removals(1,3,[("add",0,0),("add",0,1),
        ("add",0,2),("remove",0,1)]) == [1,1,1,2]
    assert intervals_overlap((1,5),(4,7))
    assert not intervals_overlap((1,5),(5,7))
    assert assign_rentals([("a",0,2),("b",2,3)])[1] == 1
    assert assign_rentals([("a",0,3),("b",1,2)],capacity=1) is None
    assert common_free_time([[(1,3)],[(2,4)]],0,5) == [(0,1),(4,5)]
    assert min_rooms_from_shards([[(0,1),(3,-1)],[(1,1),(2,-1)]]) == 2
    assert gate_crossing_times([(0,"enter"),(0,"exit"),(1,"exit")]) == [2,0,1]
    a,b = BoolNode(val=True),BoolNode(val=False)
    expression = BooleanExpression(BoolNode("OR",a,b))
    assert expression.sensitive_leaves() == [a]
    assert expression.flip(a) is False
    assert expression.flip_many([a,b]) is True
    monitor = TemperatureMinMonitor(2)
    for x in [5,1,3]:
        monitor.insert(x)
    assert monitor.minimum() == 1 and monitor.maximum() == 3
    median = SlidingMedian(3)
    for x in [1,8,2,4]:
        median.insert(x)
    assert median.median() == 4
    router = Router(["/users/{id}/photo"])
    assert route_with_parameters(router,"/users/123/photo") == (
        "/users/{id}/photo",{"id":"123"})
    methods = MethodRouter()
    methods.add("GET","/users")
    assert methods.match("GET","/users") == "/users"
    assert methods.match("POST","/users") is None
    rest = RestRouter(["/static/*","/static/{id}/photo","/static/me/settings"])
    assert rest.match("/static/me/photo") == "/static/{id}/photo"
    assert rest.match("/static/me/settings") == "/static/me/settings"
    assert rest.match("/static/other/path/file") == "/static/*"
    assert rest.match("/static") == "/static/*"
    logger = OutOfOrderMessageDeduplicator()
    assert logger.should_print(12,"x")
    assert not logger.should_print(10,"x")
    assert logger.should_print(2,"x")
    print("Concrete follow-up examples passed.")


if __name__ == "__main__":
    run_examples()
    run_followup_examples()

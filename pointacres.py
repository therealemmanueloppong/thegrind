"""Google Study Path: reference answers for Topic 1, questions 1-9.

Source: 00 STUDY PATH - Google (288).pdf, first topic.
Study this reference, then implement your own versions in learn.py.
Each section: question/examples -> brute-force explanation -> main helpers,
solution/tests -> follow-ups in PDF order with code, costs and tests.
All tests run from the entry point at the bottom. Inputs are not mutated unless
explicitly stated. N=number of cells, V=nodes, E=edges, H=houses/buildings.
BFS distances are shortest distances only when every step has equal cost.
"""

from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import count
from math import comb
import random


# ============================================================================
# SHARED CODE PATTERN: learn these three helpers first.
# ============================================================================
# Interview: "The frontier holds nodes waiting to be explored. dist stores
# both the shortest distance and whether a node has been discovered. I mark
# nodes BEFORE queueing them, so each node is queued once. I change the start
# nodes, neighbor rule, eligibility rule, and what I do with the result."
# Time O(V+E), space O(V), excluding an already supplied adjacency structure.
# For a four-neighbor grid, E=O(N), so both costs are O(N).

def frontier_search(starts, neighbors, usable=lambda v: True):
    starts = list(dict.fromkeys(starts))  # Materialize iterators; deduplicate.
    dist = {s: 0 for s in starts}  # All sources start simultaneously at 0.
    frontier = deque(starts)
    while frontier:
        u = frontier.popleft()  # BFS: nodes come out in distance order.
        # CHANGE 1: optionally act on u here in a specialized version.
        for v in neighbors(u):  # CHANGE 2: grid steps or graph adjacency.
            if v not in dist and usable(v):  # CHANGE 3: eligible cells/nodes.
                dist[v] = dist[u] + 1
                frontier.append(v)
    return dist


def grid_steps(rows, cols):
    def step(cell):
        r, c = cell
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc
    return step


def rebuild_path(parent, target):
    path = [target]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


# ============================================================================
# Q1. FLOOD FILL (LC 733)
# ============================================================================
# QUESTION: Repaint the start pixel and its four-directionally connected
# original-color region. Return the same image after mutation.
# Example: [[1,1,1],[1,1,0],[1,0,1]], start=(1,1), new=2
# -> [[2,2,2],[2,2,0],[2,0,1]]. The diagonal bottom-right 1 stays unchanged.
# Example: old == new -> return immediately; there is nothing to repaint.
# BRUTE FORCE (say): "I repeatedly scan the image, extending the marked region
# until a pass adds nothing. N passes of N pixels can cost O(N^2) time;
# a marked set needs O(N) space. A frontier avoids repeated whole-grid scans."
# MAIN HELPERS: grid_steps above. DFS is the PDF main; BFS is follow-up 1.
# MAIN: only changing popleft to pop makes a traversal DFS. Its depths would
# NOT be shortest-path distances, but flood fill only needs reachability.
# Time O(N), extra space O(N). The image is intentionally mutated.

def flood_fill(image, sr, sc, new_color):
    if not image or not image[0]:
        return image
    old = image[sr][sc]
    if old == new_color:
        return image
    neighbors = grid_steps(len(image), len(image[0]))
    frontier = deque([(sr, sc)])
    seen = {(sr, sc)}
    while frontier:
        u = frontier.pop()  # CHANGE: stack order = iterative DFS.
        r, c = u
        image[r][c] = new_color  # CHANGE 1: repaint this reached cell.
        for v in neighbors(u):
            nr, nc = v
            if v not in seen and image[nr][nc] == old:
                seen.add(v)
                frontier.append(v)
    return image


def test_q1_main():
    image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    assert flood_fill(image, 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    assert flood_fill([[0]], 0, 0, 0) == [[0]]
    assert flood_fill([], 0, 0, 2) == []


# FOLLOW-UP 1: Do it with BFS. Why is the early return needed?
# Same O(N) time/space. With recoloring as the only visited marker, old == new
# would never mark progress and cells could be requeued forever. Our dist/seen
# already prevents revisits, but the guard also avoids a useless traversal.
# The helper finds the original region before we repaint, so usable sees
# original colors throughout the search.

def flood_fill_bfs(image, sr, sc, new_color):
    if not image or not image[0]:
        return image
    old = image[sr][sc]
    if old == new_color:
        return image
    dist = frontier_search(
        [(sr, sc)], grid_steps(len(image), len(image[0])),
        usable=lambda v: image[v[0]][v[1]] == old,
    )
    for r, c in dist:
        image[r][c] = new_color
    return image


def test_q1_followups():
    assert flood_fill_bfs([[0, 0], [0, 0]], 0, 0, 5) == [[5, 5], [5, 5]]
    assert flood_fill_bfs([[1, 0], [0, 1]], 0, 0, 2) == [[2, 0], [0, 1]]
    assert flood_fill_bfs([[1]], 0, 0, 1) == [[1]]


# ============================================================================
# Q2. NUMBER OF ISLANDS (LC 200)
# ============================================================================
# QUESTION: Count components of integer 1 land; 0 is water. Four directions.
# Examples: [[1,1,0],[0,0,1]] -> 2; [[1,0],[0,1]] -> 2; [] -> 0.
# BRUTE FORCE (say): "Recursive flood fill is already O(N) time and O(N)
# stack/visited space. Its problem is recursion depth, not extra time. An
# iterative frontier avoids Python's recursion limit on a long snake island."
# MAIN HELPERS: a shared seen set between searches prevents counting one
# island more than once. Each single search still uses dist as its own seen.
# Numeric/string land is parameterized so Q4 reuses exactly this helper.
# Time O(N), space O(N). This leaves the original grid unchanged.

def island_sizes(grid, land=1):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    neighbors = grid_steps(rows, cols)
    seen, sizes = set(), []
    for r in range(rows):
        for c in range(cols):
            start = (r, c)
            if grid[r][c] != land or start in seen:
                continue
            dist = frontier_search(
                [start], neighbors,
                usable=lambda v: v not in seen and grid[v[0]][v[1]] == land,
            )
            seen.update(dist)
            sizes.append(len(dist))
    return sizes


def num_islands(grid):
    return len(island_sizes(grid))


def test_q2_main():
    assert num_islands([[1, 1, 0, 0], [1, 1, 0, 0],
                        [0, 0, 1, 1], [0, 0, 1, 1]]) == 2
    assert num_islands([[1, 0, 1], [0, 1, 0], [1, 0, 1]]) == 5
    assert num_islands([[0, 0]]) == 0
    assert num_islands([]) == 0


# FOLLOW-UP 1: Land can also be removed.
# A union-find can't split a component. Simple correct baseline: update the
# grid, then recount using the same BFS after each add/remove. K updates cost
# O(K*N) time, O(N) space. A local recount may be smaller but can still touch
# a whole island. Advanced offline option: edge lifetimes + segment tree +
# rollback DSU; this baseline does NOT claim that advanced complexity.

def island_counts_with_updates(rows, cols, updates):
    grid = [[0] * cols for _ in range(rows)]
    counts = []
    for kind, r, c in updates:
        if kind not in ("add", "remove"):
            raise ValueError("An update must be add or remove")
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError("Cell is outside the grid")
        grid[r][c] = int(kind == "add")
        counts.append(num_islands(grid))
    return counts


def test_q2_followup1():
    updates = [("add", 0, 0), ("add", 0, 2), ("add", 0, 1),
               ("remove", 0, 1), ("remove", 0, 1)]
    assert island_counts_with_updates(1, 3, updates) == [1, 2, 1, 2, 2]


# FOLLOW-UP 2: Grid too large for memory; process strips/boundary labels.
# One row is a strip. Store only the previous row, current row and a small
# union-find of boundary labels. When a component disappears from the boundary,
# it can never join future rows; count it and forget it. Compact surviving
# labels after every row. Time O(N*alpha(width)), extra space O(width).
# IMPORTANT: rows_stream must be an iterator/file source for the input itself
# to avoid O(N) memory. We accept 1 or '1' as land here.

def count_islands_stream(rows_stream):
    previous, finished, width = [], 0, None
    for row in rows_stream:
        if width is None:
            width = len(row)
            previous = [0] * width
        if len(row) != width:
            raise ValueError("Rows must have equal width")
        parent = {label: label for label in previous if label}
        size = {label: 1 for label in parent}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        current = [0] * width
        next_label = max(parent, default=0) + 1
        for c, value in enumerate(row):
            if value not in (1, "1"):
                continue
            left = current[c - 1] if c else 0
            above = previous[c]
            if not left and not above:
                parent[next_label] = next_label
                size[next_label] = 1
                current[c] = next_label
                next_label += 1
            elif left and above:
                a, b = find(left), find(above)
                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                current[c] = a
            else:
                current[c] = find(left or above)
        old_roots = {find(x) for x in previous if x}
        live_roots = {find(x) for x in current if x}
        finished += len(old_roots - live_roots)
        compact = {root: i + 1 for i, root in enumerate(live_roots)}
        previous = [compact[find(x)] if x else 0 for x in current]
    return finished + len(set(previous) - {0})


def test_q2_followup2():
    assert count_islands_stream(iter(["110", "000", "101"])) == 3
    assert count_islands_stream(iter(["101", "111"])) == 1
    assert count_islands_stream(iter([])) == 0


# FOLLOW-UP 3: Largest island area. Same searches, max instead of length.
# Time O(N), space O(N); no need for a new BFS algorithm.

def largest_island(grid):
    return max(island_sizes(grid), default=0)


def test_q2_followup3():
    assert largest_island([[1, 1, 0], [0, 1, 1]]) == 4
    assert largest_island([[0]]) == 0


# FOLLOW-UP 4: Huge grid/strips repeats follow-up 2 in the PDF.
# Reuse count_islands_stream; do not duplicate a second implementation.

def test_q2_followup4():
    assert count_islands_stream(iter(["10", "01"])) == 2


# ADDITIONAL VARIANT shown in Q2's PDF code and reused by Q4 follow-up 3:
# Land arrives one cell at a time (no deletions). This extension uses DSU,
# not a frontier, because we maintain connected groups incrementally.
# K additions: O(K*alpha(K)) amortized time, O(K) space (union by size +
# path compression). One new cell adds a group; every successful merge removes 1.
class IslandCounter:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.parent, self.size = {}, {}
        self.count = 0

    def find(self, cell):
        while self.parent[cell] != cell:
            self.parent[cell] = self.parent[self.parent[cell]]
            cell = self.parent[cell]
        return cell

    def add_land(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise ValueError("Cell is outside the grid")
        cell = (r, c)
        if cell in self.parent:
            return self.count
        self.parent[cell], self.size[cell] = cell, 1
        self.count += 1
        for nb in grid_steps(self.rows, self.cols)(cell):
            if nb not in self.parent:
                continue
            a, b = self.find(cell), self.find(nb)
            if a == b:
                continue
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]
            self.count -= 1
        return self.count


def test_q2_additions():
    islands = IslandCounter(1, 3)
    assert [islands.add_land(0, c) for c in (0, 2, 1, 1)] == [1, 2, 1, 1]


# ============================================================================
# Q3. ROTTEN ORANGES / MULTI-SOURCE BFS (TAXIS), LC 994
# ============================================================================
# QUESTION: 0 empty, 1 fresh, 2 rotten. Every minute rot crosses one grid edge.
# Return minutes until all fresh oranges rot; -1 if impossible, 0 if none fresh.
# Example [[2,1,1],[1,1,0],[0,1,1]] -> 4. [[2,0,1]] -> -1.
# BRUTE FORCE (say): "I copy the grid and scan every cell each minute so
# changes are simultaneous. This costs O(minutes*N), worst O(N^2), time and
# O(N) space. Multi-source BFS visits each cell once, rather than every minute."
# MAIN HELPERS: shared frontier_search/grid_steps.
# MAIN: CHANGE starts=all rotten cells, usable=fresh cells; distances are minutes.
# O(N) time/space, original grid unchanged.

def rotting_minutes(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    rotten = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 2]
    fresh = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
    dist = frontier_search(rotten, grid_steps(rows, cols),
                           usable=lambda v: grid[v[0]][v[1]] == 1)
    if any(cell not in dist for cell in fresh):
        return -1
    return max((dist[cell] for cell in fresh), default=0)


def test_q3_main():
    assert rotting_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert rotting_minutes([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert rotting_minutes([[0, 2]]) == 0
    assert rotting_minutes([[1]]) == -1


# FOLLOW-UP 1: Sources move/new taxis appear. Maintain distances by adding a
# source at 0 and spreading ONLY improvements. Removal/movement can INCREASE
# distances, so rebuild (not a decrease-only update). Reused by Q7.
# Helper state: dist dict is the current nearest-source distance/seen table.
# Added source: at most O(N) work per update on a degree-4 grid; rebuild O(N).
# Over K updates do NOT claim O(N) total; a cell can improve on many updates.

def grid_distances(rows, cols, sources, blocked=()):
    blocked = set(blocked)
    sources = [s for s in sources if s not in blocked]
    return frontier_search(sources, grid_steps(rows, cols),
                           usable=lambda v: v not in blocked)


def add_source_distance(rows, cols, dist, source, blocked=()):
    blocked = set(blocked)
    r, c = source
    if source in blocked or not (0 <= r < rows and 0 <= c < cols):
        raise ValueError("Source must be an open cell inside the grid")
    if dist.get(source) == 0:
        return dist
    dist[source] = 0
    frontier = deque([source])
    neighbors = grid_steps(rows, cols)
    while frontier:
        u = frontier.popleft()
        for v in neighbors(u):
            candidate = dist[u] + 1
            # CHANGE: revisit a node only if its stored distance improves.
            if v not in blocked and candidate < dist.get(v, float("inf")):
                dist[v] = candidate
                frontier.append(v)
    return dist


class SourceDistances:
    """Stores sources, walls and distances. add/remove/move update this state."""
    def __init__(self, rows, cols, sources=(), blocked=()):
        self.rows, self.cols = rows, cols
        self.blocked, self.sources = set(blocked), set(sources)
        if any(s in self.blocked or not (0 <= s[0] < rows and 0 <= s[1] < cols)
               for s in self.sources):
            raise ValueError("Sources must be inside open cells")
        self.dist = grid_distances(rows, cols, self.sources, self.blocked)

    def add(self, source):
        add_source_distance(self.rows, self.cols, self.dist, source, self.blocked)
        self.sources.add(source)
        return self.dist

    def remove(self, source):
        self.sources.discard(source)
        self.dist = grid_distances(self.rows, self.cols, self.sources, self.blocked)
        return self.dist

    def move(self, source, destination):
        r, c = destination
        if destination in self.blocked or not (0 <= r < self.rows and 0 <= c < self.cols):
            raise ValueError("Destination must be inside an open cell")
        if source not in self.sources:
            raise ValueError("Source to move is absent")
        self.sources.remove(source)
        self.sources.add(destination)
        self.dist = grid_distances(self.rows, self.cols, self.sources, self.blocked)
        return self.dist


def test_q3_followup1():
    state = SourceDistances(1, 5, [(0, 0)])
    assert state.dist[(0, 4)] == 4
    state.add((0, 4))
    assert state.dist[(0, 3)] == 1
    state.remove((0, 4))
    assert state.dist[(0, 3)] == 3
    state.move((0, 0), (0, 2))
    assert state.dist[(0, 0)] == 2


# FOLLOW-UP 2 (explanation): Why does multi-source BFS have the same cost?
# All sources enter the SAME queue at distance 0. Each new cell enters once,
# and checks four edges once. O(N), NOT sources*N. The virtual super-source
# analogy has zero-cost edges: implement it by seeding all sources at 0,
# not by adding ordinary unit-cost BFS edges and accidentally adding 1.

def test_q3_followup2():
    assert grid_distances(1, 3, [(0, 0), (0, 2)])[(0, 1)] == 1


# FOLLOW-UP 3: Signal time to all targets; optional removal of at most ONE wall.
# FOLLOW-UP 4 repeats the no-wall-removal signal-time question in the PDF.
# No targets -> 0; an unreachable target -> -1; otherwise max target distance.
# O(N+targets) time/space. Removing a blocker: enumerate each possible wall
# and run this SAME BFS. Simple correct baseline O((B+1)*N + (B+1)*targets),
# O(N+B+targets) space. One wall choice must work for ALL targets together;
# independent best walls for individual targets would answer a different task.

def signal_time(rows, cols, sources, targets, blocked=()):
    targets = list(targets)
    if not targets:
        return 0
    dist = grid_distances(rows, cols, sources, blocked)
    if any(t not in dist for t in targets):
        return -1
    return max(dist[t] for t in targets)


def signal_time_one_removal(rows, cols, sources, targets, blocked=()):
    sources, targets, walls = list(sources), list(targets), set(blocked)
    answer = signal_time(rows, cols, sources, targets, walls)
    for wall in walls:
        candidate = signal_time(rows, cols, sources, targets, walls - {wall})
        if candidate != -1 and (answer == -1 or candidate < answer):
            answer = candidate
    return answer


def test_q3_followup3():
    assert signal_time(1, 5, [(0, 0), (0, 4)], [(0, 1), (0, 2)]) == 2
    assert signal_time(1, 3, [(0, 0)], [(0, 2)], [(0, 1)]) == -1
    assert signal_time_one_removal(1, 3, [(0, 0)], [(0, 2)], [(0, 1)]) == 2


def test_q3_followup4():
    assert signal_time(1, 3, [(0, 0)], []) == 0
    assert signal_time(1, 3, [], [(0, 2)]) == -1


# ============================================================================
# Q4. SOLVE GRID AND COUNTING PROBLEMS (two separate main tasks)
# ============================================================================
# QUESTION A: count islands, but land is STRING '1', unlike numeric Q2.
# QUESTION B: choose array indices that can be rearranged to spell GOOGLE.
# Different equal-letter positions are different choices. No order restriction.
# Examples: ['1'] -> one island; list('GOOGLE') -> 1 selection;
# list('GOOOGLE') -> 3 (choose two of the three O positions).
# BRUTE FORCE (say): "For islands, recursive flood fill is already O(N) but
# risks deep recursion. For the letters, I enumerate all six-position subsets
# and check their letters: O(C(L,6)) time, O(1) extra for fixed word size.
# Instead I count letters once and multiply the choices for each letter."
# MAIN HELPERS: Q2 island_sizes with land='1'; Counter and comb for task B.

def grid_count_islands(grid):
    # O(N) time/space; same frontier pattern, only usable's land value changes.
    return len(island_sizes(grid, land="1"))


def ways_to_spell(letters, word="GOOGLE"):
    # O(L + W) counting + one binomial per distinct target letter.
    # O(U) counters, where U is distinct letters. For fixed uppercase alphabet
    # and fixed GOOGLE, auxiliary space O(1). Arithmetic on big ints is not
    # constant-cost at enormous input sizes; standard bounds count operations.
    have, need = Counter(letters), Counter(word)
    answer = 1
    for ch, required in need.items():
        if have[ch] < required:
            return 0
        answer *= comb(have[ch], required)
    return answer


def test_q4_main():
    assert grid_count_islands([]) == 0
    assert grid_count_islands([["1"]]) == 1
    assert grid_count_islands(["11000", "11000", "00100", "00011"]) == 3
    assert ways_to_spell([]) == 0
    assert ways_to_spell(list("GOOGLE")) == 1
    assert ways_to_spell(list("GOOOGLE")) == 3
    assert ways_to_spell(list("GGGOOLEE")) == 6


# FOLLOW-UP 1: Any target word. ways_to_spell already parameterizes the target.
# Product C(available, needed) counts sets of indices, not permutations.

def test_q4_followup1():
    assert ways_to_spell("AABB", "AB") == 4
    assert ways_to_spell("AABB", "AAA") == 0
    assert ways_to_spell("ABC", "") == 1  # One empty selection.


# FOLLOW-UP 2: Letters must appear in order (subsequence).
# Extension needs DP instead of BFS. ways[j] counts the ways to make word[:j].
# Update j BACKWARD so one input letter cannot be reused in this iteration.
# O(L*W) time, O(W) space. Example 'AAA' -> 'AA' has 3 subsequences.

def ways_in_order(letters, word="GOOGLE"):
    ways = [1] + [0] * len(word)
    for ch in letters:
        for j in range(len(word), 0, -1):
            if ch == word[j - 1]:
                ways[j] += ways[j - 1]
    return ways[-1]


def test_q4_followup2():
    assert ways_in_order("GOOGLE") == 1
    assert ways_in_order("GGOOGLE") == 2
    assert ways_in_order("GOGOLE") == 0
    assert ways_in_order("AAA", "AA") == 3
    assert ways_in_order("ABC", "") == 1


# FOLLOW-UP 3: Islands arrive one cell at a time.
# Helper: IslandCounter above (Q2). Main wrapper returns a count after each add.
# O(K*alpha(K)) time, O(K) space. Repeated additions are no-ops.

def islands_after_additions(rows, cols, additions):
    islands = IslandCounter(rows, cols)
    return [islands.add_land(r, c) for r, c in additions]


def test_q4_followup3():
    assert islands_after_additions(1, 3, [(0, 0), (0, 2), (0, 1)]) == [1, 2, 1]
    assert islands_after_additions(1, 1, [(0, 0), (0, 0)]) == [1, 1]


# ============================================================================
# QUESTION 5: Find shortest relationship path using BFS
# PDF: Google (288), Topic 1, question 5. adj maps people to outgoing neighbors.
# Return a shortest chain including both endpoints, or None if unreachable.
# Example: a -> b -> c returns [a,b,c]; a to a returns [a].
# BRUTE FORCE: "I could enumerate simple paths and keep the shortest. There
# can be factorially many paths, so I use BFS to discover shortest paths first."
# Brute auxiliary space O(V) excluding output. MAIN: O(V+E) time, O(V) space.
# MAIN helpers: rebuild_path above. CHANGE: record parent on discovery.

def shortest_path(adj, s, t):
    dist, parent = {s: 0}, {s: None}
    frontier = deque([s])
    while frontier:
        u = frontier.popleft()
        if u == t:
            return rebuild_path(parent, t)
        for v in adj.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                frontier.append(v)
    return None


def test_q5_main():
    adj = {'ann': ['bob', 'cy'], 'bob': ['dee'], 'cy': ['dee', 'eli'],
           'dee': ['fay'], 'eli': ['fay'], 'fay': []}
    assert shortest_path(adj, 'ann', 'fay') == ['ann', 'bob', 'dee', 'fay']
    assert shortest_path(adj, 'ann', 'ann') == ['ann']
    assert shortest_path(adj, 'fay', 'ann') is None


# FOLLOW-UP 1: Huge graph: search from both ends. Return shortest distance.
# For directed relationships the target search MUST use reversed edges.
# Expand a complete layer of the smaller frontier. Typical work is roughly
# b**(d/2) per side; worst case O(V+E) time/space including reverse adjacency.
# Example a->b->c: the searches meet at b, distance 2.
# Helper addition: reverse adjacency; main: bidirectional layer expansion.

def reverse_graph(adj):
    reverse = defaultdict(list)
    for u, neighbors in adj.items():
        for v in neighbors:
            reverse[v].append(u)
    return reverse


def bidirectional(adj, s, t):
    if s == t:
        return 0
    reverse = reverse_graph(adj)
    left, right = {s}, {t}
    ds, dt = {s: 0}, {t: 0}
    while left and right:
        forward = len(left) <= len(right)
        layer, own, other, graph = (left, ds, dt, adj) if forward else (right, dt, ds, reverse)
        next_layer, best = set(), None
        for u in layer:
            for v in graph.get(u, []):
                if v not in own:
                    own[v] = own[u] + 1
                    next_layer.add(v)
                if v in other:
                    candidate = own[v] + other[v]
                    best = candidate if best is None else min(best, candidate)
        if best is not None:
            return best
        if forward:
            left = next_layer
        else:
            right = next_layer
    return None


def test_q5_followup1():
    adj = {'a': ['b'], 'b': ['c'], 'c': []}
    assert bidirectional(adj, 'a', 'c') == 2
    assert bidirectional(adj, 'c', 'a') is None
    assert bidirectional(adj, 'a', 'a') == 0


# FOLLOW-UP 2: All shortest chains, or their count.
# Keep ALL parents that lead to the same shortest distance. Count paths as
# nodes are discovered in BFS order; list paths by walking parents backward.
# Example a->b/d and b/d->c gives two shortest paths, each length 2.
# Helper/count: O(V+E) time/space (unit-cost integer arithmetic).
# Listing additionally costs O(P*L) time/output space for P paths of length L.
# The number of paths, and therefore the output, can be exponential.

def shortest_parent_dag(adj, s):
    dist, parents, ways = {s: 0}, {s: []}, {s: 1}
    frontier = deque([s])
    while frontier:
        u = frontier.popleft()
        for v in dict.fromkeys(adj.get(u, [])):
            if v not in dist:
                dist[v], parents[v], ways[v] = dist[u] + 1, [], 0
                frontier.append(v)
            if dist[v] == dist[u] + 1:
                parents[v].append(u)
                ways[v] += ways[u]
    return parents, ways


def count_shortest_paths(adj, s, t):
    _, ways = shortest_parent_dag(adj, s)
    return ways.get(t, 0)


def all_shortest_paths(adj, s, t):
    parents, ways = shortest_parent_dag(adj, s)
    if t not in ways:
        return []
    result = []
    def collect(u, backwards):
        if u == s:
            result.append(backwards[::-1])
            return
        for p in parents[u]:
            backwards.append(p)
            collect(p, backwards)
            backwards.pop()
    collect(t, [t])
    return result


def test_q5_followup2():
    adj = {'a': ['b', 'd', 'b'], 'b': ['c'], 'd': ['c']}
    assert all_shortest_paths(adj, 'a', 'c') == [['a', 'b', 'c'], ['a', 'd', 'c']]
    assert count_shortest_paths(adj, 'a', 'c') == 2
    assert all_shortest_paths(adj, 'a', 'a') == [['a']]
    assert count_shortest_paths(adj, 'c', 'a') == 0


# FOLLOW-UP 3: Nonnegative weighted relationships: replace FIFO with a heap.
# Distances may improve, so "not seen" becomes "new distance is smaller".
# Example a->b cost1, b->c cost1, a->c cost5: answer (2,[a,b,c]).
# Helper is also reused by Q6. Lazy heap: O((V+E)log(V+E)) time,
# O(V+E) extra space; negative edge weights are not supported.

def dijkstra_sources(adj, starts):
    for neighbors in adj.values():
        if any(weight < 0 for _, weight in neighbors):
            raise ValueError('Dijkstra requires nonnegative weights')
    serial = count()
    dist = {s: 0 for s in starts}
    parent = {s: None for s in dist}
    frontier = [(0, next(serial), s) for s in dist]
    # All initial priorities are zero and serials increase, so this is a heap.
    while frontier:
        distance, _, u = heappop(frontier)
        if distance != dist[u]:
            continue
        for v, weight in adj.get(u, []):
            candidate = distance + weight
            if candidate < dist.get(v, float('inf')):
                dist[v], parent[v] = candidate, u
                heappush(frontier, (candidate, next(serial), v))
    return dist, parent


def weighted_path(adj, s, t):
    dist, parent = dijkstra_sources(adj, [s])
    return (dist[t], rebuild_path(parent, t)) if t in dist else None


def test_q5_followup3():
    adj = {'a': [('b', 1), ('c', 5)], 'b': [('c', 1)]}
    assert weighted_path(adj, 'a', 'c') == (2, ['a', 'b', 'c'])
    assert weighted_path(adj, 'c', 'a') is None
    assert weighted_path({'a': [('b', 0)]}, 'a', 'b') == (0, ['a', 'b'])


# ============================================================================
# QUESTION 6: Farthest City for a New Data Center
# PDF: Topic 1 Q6. Undirected roads, city IDs 0..n-1, nonempty center list.
# Every city is reachable from some center. Return city farthest from its
# NEAREST center, breaking ties by smallest city ID.
# Example path 0-1-2-3-4, centers [0,4]: answer 2.
# BRUTE FORCE: "I run BFS from each of D centers, then keep each city's minimum
# distance. That costs O(D*(V+E)). Starting every center together reduces it
# to one BFS, O(V+E)." Graph plus frontier use O(V+E) space.
# MAIN helper: build roads. CHANGE starts=all centers; neighbors=adj[u].

def city_graph(n, edges, weighted=False):
    adj = {u: [] for u in range(n)}
    for edge in edges:
        a, b = edge[:2]
        if weighted:
            adj[a].append((b, edge[2]))
            adj[b].append((a, edge[2]))
        else:
            adj[a].append(b)
            adj[b].append(a)
    return adj


def farthest_city(num_cities, edges, dcs):
    adj = city_graph(num_cities, edges)
    dist = frontier_search(dcs, lambda u: adj[u])
    if len(dist) != num_cities or not dist:
        raise ValueError('Each city must be reachable from a data center')
    return min(dist, key=lambda u: (-dist[u], u))


def test_q6_main():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert farthest_city(5, edges, [0, 4]) == 2
    assert farthest_city(5, edges, [0]) == 4
    assert farthest_city(4, [(0, 1), (1, 2), (2, 3)], [0, 3]) == 1


# FOLLOW-UP 1: Weighted roads: all centers enter Dijkstra with distance zero.
# Reuse dijkstra_sources. Example weights 2 then 5, center0: city2 is farthest.
# O((V+E)log(V+E)) time, O(V+E) space including adjacency and lazy heap.

def farthest_city_weighted(num_cities, edges, dcs):
    dist, _ = dijkstra_sources(city_graph(num_cities, edges, True), dcs)
    if len(dist) != num_cities or not dist:
        raise ValueError('Each city must be reachable from a data center')
    return min(dist, key=lambda u: (-dist[u], u))


def test_q6_followup1():
    assert farthest_city_weighted(3, [(0, 1, 2), (1, 2, 5)], [0]) == 2
    assert farthest_city_weighted(3, [(0, 1, 2), (1, 2, 5)], [0, 2]) == 1


# ============================================================================
# QUESTION 7: Compute distance to nearest taxi in grid
# PDF: Topic 1 Q7. T=taxi, #=wall, .=open. Return distance matrix; -1 means
# wall or unreachable. Example T.. -> [0,1,2]; no taxi -> all -1.
# BRUTE FORCE: "BFS separately from each open cell can cost O(N squared).
# I start from all taxis together so each cell is discovered once: O(N)."
# Space O(N). MAIN helpers: grid_steps/frontier_search, as in Q3.

def taxi_distances(grid):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    starts = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'T']
    dist = frontier_search(starts, grid_steps(rows, cols), lambda v: grid[v[0]][v[1]] != '#')
    return [[dist.get((r, c), -1) for c in range(cols)] for r in range(rows)]


def test_q7_main():
    assert taxi_distances(['T.#', '...', '#.T']) == [[0, 1, -1], [1, 2, 1], [-1, 1, 0]]
    assert taxi_distances(['..']) == [[-1, -1]]
    assert taxi_distances(['T#.']) == [[0, -1, -1]]


# FOLLOW-UP 1: Add a taxi. MUTATES grid and its supplied distance matrix.
# Spread only improvements from the new zero-distance cell, O(N) worst time
# and space. Example T.... plus taxi at column4 -> [0,1,2,1,0].
# Helper: set_grid_cell also supports rows supplied as strings.

def set_grid_cell(grid, r, c, value):
    if isinstance(grid[r], str):
        grid[r] = list(grid[r])
    grid[r][c] = value


def add_taxi(grid, distances, r, c):
    if grid[r][c] == '#':
        raise ValueError('Cannot place a taxi on a wall')
    set_grid_cell(grid, r, c, 'T')
    distances[r][c] = 0
    frontier = deque([(r, c)])
    neighbors = grid_steps(len(grid), len(grid[0]))
    while frontier:
        u = frontier.popleft()
        for nr, nc in neighbors(u):
            candidate = distances[u[0]][u[1]] + 1
            if grid[nr][nc] != '#' and (distances[nr][nc] == -1 or candidate < distances[nr][nc]):
                distances[nr][nc] = candidate
                frontier.append((nr, nc))
    return distances


def test_q7_followup1():
    grid = ['T....']
    distances = taxi_distances(grid)
    assert add_taxi(grid, distances, 0, 4) == [[0, 1, 2, 1, 0]]
    assert distances == taxi_distances(grid)


# FOLLOW-UP 2: Removing/moving a taxi can INCREASE distances. The decrease-only
# queue is insufficient. Simple baseline: mutate sources and rebuild O(N)
# time/space. Example T.T remove left taxi -> [2,1,0].

def remove_taxi(grid, r, c):
    if grid[r][c] != 'T':
        raise ValueError('No taxi at this cell')
    set_grid_cell(grid, r, c, '.')
    return taxi_distances(grid)


def move_taxi(grid, old, new):
    if grid[old[0]][old[1]] != 'T' or grid[new[0]][new[1]] == '#':
        raise ValueError('Invalid taxi move')
    set_grid_cell(grid, *old, '.')
    set_grid_cell(grid, *new, 'T')
    return taxi_distances(grid)


def test_q7_followup2():
    grid = ['T.T']
    assert remove_taxi(grid, 0, 0) == [[2, 1, 0]]
    assert move_taxi(grid, (0, 2), (0, 1)) == [[1, 0, 1]]
    assert remove_taxi(grid, 0, 1) == [[-1, -1, -1]]


# FOLLOW-UP 3: Also identify the nearest taxi. Assign row-major taxi IDs.
# Copy owner[u] to owner[v] on discovery. Initial row-major order resolves ties
# to the smallest taxi ID. None means wall/unreachable. O(N) time/space.
# Example T.T: owners [0,0,1], the middle cell ties and chooses taxi0.

def nearest_taxi_ids(grid):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    starts = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'T']
    dist = {s: 0 for s in starts}
    owner = {s: i for i, s in enumerate(starts)}
    frontier = deque(starts)
    neighbors = grid_steps(rows, cols)
    while frontier:
        u = frontier.popleft()
        for v in neighbors(u):
            if v not in dist and grid[v[0]][v[1]] != '#':
                dist[v], owner[v] = dist[u] + 1, owner[u]
                frontier.append(v)
    return [[owner.get((r, c)) for c in range(cols)] for r in range(rows)]


def test_q7_followup3():
    assert nearest_taxi_ids(['T.T']) == [[0, 0, 1]]
    assert nearest_taxi_ids(['T#.']) == [[0, None, None]]


# ============================================================================
# QUESTION 8: Infection Spread on a Grid (Cellular Automaton)
# PDF: Topic 1 Q8. I=infected, .=healthy; other symbols block spread.
# Return rounds until NO NEW infection occurs. Unreachable healthy cells do
# not cause -1. Example I... ->3 rounds; I#. ->0 rounds.
# BRUTE FORCE: "I could copy and scan the entire grid each round: O(S*N),
# up to O(N squared). BFS processes only newly infected cells: O(N)."
# Space O(N). MAIN helper returns infection times; main returns their maximum.

def infection_times(grid):
    if not grid or not grid[0]:
        return {}
    rows, cols = len(grid), len(grid[0])
    starts = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'I']
    return frontier_search(starts, grid_steps(rows, cols), lambda v: grid[v[0]][v[1]] == '.')


def spread_steps(grid):
    return max(infection_times(grid).values(), default=0)


def test_q8_main():
    assert spread_steps(['I...']) == 3
    assert spread_steps(['I..', '...', '..#']) == 3
    assert spread_steps(['I#.']) == 0
    assert spread_steps(['...']) == 0


# FOLLOW-UP 1: Recover d rounds after infection, with permanent immunity.
# Convention: d>=1; a cell can transmit next round before recovering that
# round. Thus infection times stay the same; at t>=infection_time+d it is R.
# Example I.. with d=1: at t1 RI.; at t2 RRI. O(N) time/space per state query.
# MAIN uses the infection_times helper, then renders the requested snapshot.

def grid_at(grid, t, recovery=None):
    if t < 0 or (recovery is not None and recovery < 1):
        raise ValueError('Time must be nonnegative; recovery delay must be positive')
    when = infection_times(grid)
    result = [list(row) for row in grid]
    for (r, c), infected_at in when.items():
        if infected_at <= t:
            result[r][c] = 'R' if recovery is not None and t >= infected_at + recovery else 'I'
    return [''.join(row) for row in result]


def test_q8_followup1():
    assert grid_at(['I..'], 1, recovery=1) == ['RI.']
    assert grid_at(['I..'], 2, recovery=1) == ['RRI']
    assert grid_at(['I..'], 3, recovery=1) == ['RRR']


# FOLLOW-UP 2: Early exit when no cell changes.
# The basic BFS already stops when its frontier empties: no new infections.
# With recovery, pending recoveries can still change the grid afterward.
# Final stabilization time is last infection + d, or 0 if no infection exists.
# O(N) time/space, reusing infection_times. I.., d2 stabilizes at time4.

def stabilization_steps(grid, recovery=None):
    when = infection_times(grid)
    if recovery is not None and recovery < 1:
        raise ValueError('Recovery delay must be positive')
    return max(when.values()) + (recovery or 0) if when else 0


def test_q8_followup2():
    assert stabilization_steps(['I..'], 2) == 4
    assert stabilization_steps(['I#.']) == 0
    assert stabilization_steps(['...'], 2) == 0


# FOLLOW-UP 3: Probabilistic spread: each infected-to-healthy edge retries
# independently each round with probability p. Newly infected cells spread
# only in the NEXT round. A failed round does not mean permanent stability.
# Use an explicit max_steps cap (p=0 must not loop forever) and seeded RNG.
# Return (infection_times, finished), where finished means no possible edge
# remains. O(max_steps*N) worst time, O(N) space. p1 matches deterministic BFS.

def probabilistic_infection(grid, probability, max_steps, seed=0):
    if not 0 <= probability <= 1 or max_steps < 0:
        raise ValueError('Invalid probability or step limit')
    if not grid or not grid[0]:
        return {}, True
    rng = random.Random(seed)
    neighbors = grid_steps(len(grid), len(grid[0]))
    when = {(r, c): 0 for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 'I'}
    def susceptible(v):
        return v not in when and grid[v[0]][v[1]] == '.'
    for step in range(1, max_steps + 1):
        newly, possible = set(), False
        for u in sorted(when):
            for v in neighbors(u):
                if susceptible(v):
                    possible = True
                    if rng.random() < probability:
                        newly.add(v)
        if not possible:
            return when, True
        for v in newly:
            when[v] = step
    finished = not any(susceptible(v) for u in when for v in neighbors(u))
    return when, finished


def test_q8_followup3():
    when, finished = probabilistic_infection(['I...'], 1, 3)
    assert when == infection_times(['I...']) and finished
    assert probabilistic_infection(['I.'], 0, 5) == ({(0, 0): 0}, False)
    assert probabilistic_infection(['I#.'], 0, 5) == ({(0, 0): 0}, True)
    assert probabilistic_infection(['I...'], .5, 10, 9) == probabilistic_infection(['I...'], .5, 10, 9)


# ============================================================================
# QUESTION 9: Shortest Distance From All Buildings
# PDF: Topic 1 Q9. 0=empty, 1=building, 2=obstacle. Return the best EMPTY CELL
# coordinates, not the total distance. Minimize sum of distances to ALL houses;
# break ties in row-major order; impossible ->(-1,-1). Houses block transit.
# Example [[1,0,1]] ->(0,1); [[1,2,1]] ->(-1,-1).
# BRUTE FORCE: "From each of Z empty cells I could BFS to every building,
# costing O(Z*N). Instead I BFS from each of H buildings and accumulate each
# empty cell's total: O(H*N). This helps when H is smaller than Z; both can
# be O(N squared) in the worst case." Auxiliary space O(N).
# MAIN helper: one frontier_search per building, only empty neighbors usable.
# Do NOT seed all buildings together: that gives nearest distance, not SUM.

def school_totals(grid):
    if not grid or not grid[0]:
        return [], [], 0
    rows, cols = len(grid), len(grid[0])
    total = [[0] * cols for _ in range(rows)]
    reached = [[0] * cols for _ in range(rows)]
    houses = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
    for house in houses:
        dist = frontier_search([house], grid_steps(rows, cols), lambda v: grid[v[0]][v[1]] == 0)
        for (r, c), distance in dist.items():
            if grid[r][c] == 0:
                total[r][c] += distance
                reached[r][c] += 1
    return total, reached, len(houses)


def choose_school(grid, total, reached, houses):
    best, best_sum = (-1, -1), float('inf')
    if houses == 0:
        return best
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 0 and reached[r][c] == houses and total[r][c] < best_sum:
                best, best_sum = (r, c), total[r][c]
    return best


def shortest_distance_from_all_buildings(grid):
    total, reached, houses = school_totals(grid)
    return choose_school(grid, total, reached, houses)


def test_q9_main():
    grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
    assert shortest_distance_from_all_buildings(grid) == (1, 2)
    assert shortest_distance_from_all_buildings([[1, 0, 1]]) == (0, 1)
    assert shortest_distance_from_all_buildings([[1, 2, 1]]) == (-1, -1)
    assert shortest_distance_from_all_buildings([[0, 1, 1, 0]]) == (-1, -1)
    assert shortest_distance_from_all_buildings([[1, 0], [0, 1]]) == (0, 1)


# FOLLOW-UP 1: Minimize average rather than sum. Every eligible cell reaches
# the same H buildings, so dividing by H preserves the minimizing cell.
# Reuse totals and choose_school; return (coordinates, average), None average
# when impossible. Example [1,0,1] ->((0,1),1.0). O(H*N) time/O(N) space.

def best_school_average(grid):
    total, reached, houses = school_totals(grid)
    spot = choose_school(grid, total, reached, houses)
    return (spot, None) if spot == (-1, -1) else (spot, total[spot[0]][spot[1]] / houses)


def test_q9_followup1():
    assert best_school_average([[1, 0, 1]]) == ((0, 1), 1.0)
    assert best_school_average([[1, 2, 1]]) == ((-1, -1), None)


def run_all_tests():
    tests = [fn for name, fn in globals().items() if name.startswith('test_') and callable(fn)]
    for test in tests:
        test()
    print(f'All {len(tests)} test groups passed for questions 1-9 and their follow-ups.')


if __name__ == '__main__':
    run_all_tests()

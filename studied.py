# Question 1: Friend Graph with Timeline
# MAIN QUESTION ONLY: friendships are added; no unfriend events yet.
# People are numbered 0 through n - 1.
# Each event is (time, person_a, person_b, "friend").
# Return the earliest time everyone belongs to one connected group.
# Return -1 if that never happens; for one person, return 0.


def earliest_all_connected(n, events):
    # TODO: Build your solution here, one step at a time.
    if n <= 1:
        return 0
    groups = n
    parent =  list(range(n))
    size = [1] * n
    def findparent(x):
        if parent[x] == x:
            return x
        parent[x] = findparent(parent[x])
        return parent[x]

    data = sorted(events, key = lambda x : x[0])
    for time, a, b, kind in data:
        pa = findparent(a)
        pb = findparent(b)

        if pa != pb:
            if size[pa] < size[pb]:
                parent[pa] = pb
                size[pb] += size[pa]

            else:
                parent[pb] = pa
                size[pa] += size[pb]
            groups-=1

            if groups == 1:
                return time

    return -1


if __name__ == "__main__":
    # Write your test cases here.
    assert(earliest_all_connected(1,[])) == 0
    assert(earliest_all_connected(2,[])) == -1
    assert(earliest_all_connected(2,[(4,0,1, 'friend')])) == 4
    assert(earliest_all_connected(3,[(5, 1, 2, "friend"),(1, 0, 1, "friend")])) == 5
    assert(earliest_all_connected(3,[(1, 0, 1, "friend"),(2, 0, 1, "friend")])) == -1


# Question 2: Maximum-Area Rectangle from Planar Points
# MAIN QUESTION ONLY; follow-ups come after both main-question passes.
# Input: a list of points, each represented as (x, y).
# Choose four given points that form a rectangle. Tilted rectangles are allowed.
# Return the largest possible rectangle area, or 0 if no rectangle exists.
# Example: [(0, 0), (3, 0), (3, 2), (0, 2)] -> 6.


from collections import defaultdict
def max_rect_area(points):
    # TODO: Write your solution here as we work through it together.
    if len(points) < 4:
        return 0

    pts = []
    data = set()

    for x,y in points:
        if (x,y) not in data:
            data.add((x,y))
            pts.append((x,y))

    G = defaultdict(list)

    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            x1, y1 = pts[i]
            x2,y2 = pts[j]

            xsum = x1+x2
            ysum = y1+y2

            xdiff = x2-x1
            ydiff = y2-y1

            diagonalsq = xdiff**2 + ydiff**2
            key = (xsum, ysum, diagonalsq)

            G[key].append((x1,y1,x2,y2))


    best = 0
    for v in G.values():
        for i in range(len(v)):
            x1,y1,x2,y2 = v[i]
            for j in range(i+1, len(v)):
                xo1, yo1, xo2,yo2 = v[j]

                x1diff = x1-xo1
                y1diff = y1 - yo1

                x2diff = x1-xo2
                y2diff = y1 - yo2


                area = abs((x1diff * y2diff) - (x2diff * y1diff))
                best = max(area, best)

    return best










if __name__ == "__main__":
    # Write your own test cases here when your solution is finished.
    assert(max_rect_area([])) == 0
    assert(max_rect_area([(0, 0), (3, 0), (3, 2), (0, 2)])) == 6
    assert(max_rect_area([(0, 0), (0, 0), (0, 0), (0, 0)])) == 0
    assert(max_rect_area([(0, 0), (1, 1), (0, 2), (-1, 1)])) == 2
    assert(max_rect_area([(0, 0), (3, 0), (0, 1), (3, 1), (0, 2), (3, 2)])) == 6


# Question 3: Course Scheduling and Dependency Variants
# CURRENT MAIN VERSION: merge two ordered sequences.
# Input: two lists of integer labels, a and b.
# Each list says its values must appear in that relative order.
# A shared value represents the same item in both lists.
# Return True if one combined order can satisfy both lists, otherwise False.
# For this version, assume each list contains distinct labels.
# Example: a=[1,2,3], b=[2,4,5] -> True; [1,2,3,4,5] is a valid order.
# Example: a=[1,6,4], b=[4,1] -> False; the rules create a cycle.
# MAIN QUESTION ONLY. Follow-ups come after both main-question passes.


from collections import defaultdict, deque

def can_merge_orders(a, b):
    # TODO: Build your solution with guided questions.
    if not a and not b:
        return True


    edges = []
    for arr in (a,b):
        for i in range(len(arr)-1):
            edges.append((arr[i],arr[i+1]))



    G = defaultdict(list)
    for arr in (a,b):
        for i in range(len(arr)):
            G[arr[i]] = []


    for u,v in edges:
        G[u].append(v)


    indegree = {}
    for arr in (a,b):
        for i in range(len(arr)):
            indegree[arr[i]] = 0


    for u,v in edges:
        indegree[v] += 1


    q =  deque(u for u,v in G.items() if indegree[u] == 0 )
    order = []

    #bfs
    while q:
        node = q.popleft()
        order.append(node)

        for nb in G[node]:
            indegree[nb] -=1
            if indegree[nb] == 0:
                q.append(nb)


    return len(order) == len(G)







# EXAMPLES: ALL ITEMS versus ORDERING PAIRS
# Example 1:
# a = [1, 2, 3]
# b = []
# edges = [(1, 2), (2, 3)]
# All required items: 1, 2, 3.
# Your neighbor dictionary has 1:[2], 2:[3]; 3 still needs to be included.
#
# Example 2:
# a = [42]
# b = []
# edges = []
# All required items: 42.
# No pairs exist, but the combined order [42] is valid.
# Therefore: collect items from the input lists; use edges for relationships.


if __name__ == "__main__":
    # Write your own test cases when your solution is finished.
    assert(can_merge_orders([], [])) == True
    assert(can_merge_orders([42], [])) == True

    # Next test inputs: write your assertion underneath these lines.
    a = [1, 2, 3]
    b = [2, 4, 5]
    assert(can_merge_orders(a,b)) == True

    # Next test: conflicting ordering rules.
    a_conflict = [1, 6, 4]
    b_conflict = [4, 1]
    # Write your assertion here after deciding the expected result.
    assert(can_merge_orders(a_conflict,b_conflict)) == False

    # Next test: both lists repeat the same ordering rule.
    a_same = [1, 2]
    b_same = [1, 2]
    # Write your assertion after deciding whether these rules conflict.
    assert(can_merge_orders(a_same,b_same)) == True


# ============================================================
# QUESTION 4: CONNECTED CROP ARRANGEMENT ON A GRID
# ============================================================
# Build one edge-adjacent path through every cell, then place each crop's
# required cells consecutively along that path. Consecutive cells in the path
# share an edge, so each crop's consecutive segment is connected.
def arrange_crops(n, m, counts):
    rows = n
    cols = m
    if not rows:
        return []
    grid = [[0] * cols for r in range(rows)]

    path = []
    for r in range(rows):
        if r % 2 == 0:
            for c in range(cols):
                path.append([r, c])
        else:
            for c in reversed(range(cols)):
                path.append([r, c])

    k = 0
    for i, num in enumerate(counts):
        for j in range(num):
            x, y = path[k]
            grid[x][y] = i + 1
            k += 1

    return grid


if __name__ == "__main__":
    ans = arrange_crops(2, 3, [4, 2])
    assert ans == [[1, 1, 1], [2, 2, 1]]
    ans = arrange_crops(1, 4, [2, 2])
    assert ans == [[1, 1, 2, 2]]
    ans = arrange_crops(2, 3, [2, 2, 2])
    assert ans == [[1, 1, 2], [3, 3, 2]]
    ans = arrange_crops(2, 2, [4])
    assert ans == [[1, 1], [1, 1]]


# ============================================================
# QUESTION 5: LONGEST NON-DECREASING SUBARRAY WITH ONE CHANGE
# ============================================================
def longest_with_one_change(nums):
    if not nums:
        return 0

    n = len(nums)
    if n <= 2:
        return n

    left = [1] * n
    right = [1] * n
    for i in range(1, n):
        if nums[i] >= nums[i - 1]:
            left[i] = left[i - 1] + 1

    for i in reversed(range(n - 1)):
        if nums[i] <= nums[i + 1]:
            right[i] = right[i + 1] + 1

    best = 1
    for i in range(n):
        leftval = left[i - 1] if i > 0 else 0
        rightval = right[i + 1] if i < n - 1 else 0
        if i == 0 or i == n - 1 or nums[i - 1] <= nums[i + 1]:
            ans = leftval + rightval + 1
        else:
            ans = max(leftval, rightval) + 1
        best = max(best, ans)

    return best


if __name__ == "__main__":
    nums = [1, 0, 3, 4, 5, 2, 3]
    assert longest_with_one_change(nums) == 5
    nums = []
    assert longest_with_one_change(nums) == 0
    nums = [1, 2, 3, 4]
    assert longest_with_one_change(nums) == 4
    nums = [4, 3, 2, 1]
    assert longest_with_one_change(nums) == 2



========================================================================

# Question 6: Number of Islands
# MAIN QUESTION ONLY. Follow-ups come after both main-question passes.
#
# Given a grid containing '1' for land and '0' for water, count the number of
# islands. An island is a group of land cells connected up, down, left, or
# right. Diagonal contact does not count.


def num_islands(grid):
    # TODO: Build the main solution with guided questions.
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    def inbounds(r,c):
        return 0<=r<rows and 0<=c<cols

    def dfs(r,c):
        if not inbounds(r,c):
            return

        if grid[r][c] == '0':
            return

        grid[r][c] = '0'
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if inbounds(nr,nc):
                dfs(nr, nc)

    rows = len(grid)

    if rows == 0:
        return 0

    cols = len(grid[0])

    if cols == 0:
        return 0

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r,c)

    return count


if __name__ == "__main__":
    # Test 1: the example grid has two islands.
    # grid = [
    #     ['1', '1', '0', '0'],
    #     ['1', '0', '0', '1'],
    #     ['0', '0', '1', '1'],
    # ]
    # Expected result: 2
    grid = [
        ['1', '1', '0', '0'],
        ['1', '0', '0', '1'],
        ['0', '0', '1', '1'],
    ]
    assert(num_islands(grid)) == 2

    # Test 2: an empty grid has no islands.
    # grid = []
    # Expected result: 0
    grid = []
    assert(num_islands(grid)) == 0

    # Test 3: a grid with rows but no columns has no islands.
    # grid = [[]]
    # Expected result: 0
    grid = [[]]
    assert(num_islands(grid)) == 0

    # Test 4: all water means no islands.
    # grid = [['0', '0'], ['0', '0']]
    # Expected result: 0
    grid = [['0', '0'], ['0', '0']]
    assert(num_islands(grid)) == 0

    # Test 5: all land connected together is one island.
    # grid = [['1', '1'], ['1', '1']]
    # Expected result: 1
    grid = [['1', '1'], ['1', '1']]
    assert(num_islands(grid)) == 1


    # Test 6: diagonal land cells do not connect.
    # grid = [['1', '0'], ['0', '1']]
    # Expected result: 2
    grid = [['1', '0'], ['0', '1']]
    assert(num_islands(grid)) == 2


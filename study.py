# Question 11: Grid Path Count with Diagonal Moves and Checkpoints
# MAIN QUESTION ONLY. Follow-ups come after both main-question passes.
#
# Main question: Count paths in an n x m matrix from (n - 1, 0) to
# (n - 1, m - 1). From (r, c), the allowed moves are up-right,
# right, and down-right. Stay inside the matrix and return the number of
# distinct paths.
#
# Every move advances exactly one column to the right.
#
# Example 1:
# n = 1, m = 4
# Expected result: 1
# With one row, the only path moves right across every column.
#
# Example 2:
# n = 3, m = 3
# Expected result: 2
# The path starts at row 2, column 0, and must return to row 2 at column 2.
#
# The PDF also lists checkpoint follow-ups. They come only after all 26 main
# questions.

def count_paths(n, m):
    # TODO: Build the main solution with guided questions.
    # Hint: the rolling state represents one current column, so it needs one count per row.
    def inbounds(r):
        return 0<=r<rows
    rows = n
    cols = m
    ways = [0]* rows
    ways[rows-1] = 1
    for c in range(1, cols):
        nextways = [0]*rows
        for r in range(rows):
            nextways[r]=ways[r]
            if inbounds(r-1):
                nextways[r]= ways[r]+ways[r-1]

            if inbounds(r+1):
                nextways[r] += ways[r+1]

        # Question: after every row in this column is computed, which variable
        # should become the new current-column state?
        # Hint: the next column must use nextways instead of the old ways.
        ways = nextways

    # Question: after all columns are processed, which row contains the target?
    # Hint: the target is on the bottom row.

if __name__ == "__main__":
    # Test 1: one row gives one straight path.
    # assert count_paths(1, 4) == 1

    # Test 2: three rows and three columns.
    # assert count_paths(3, 3) == 2

    # Test 3: one column has only the starting cell.
    # assert count_paths(3, 1) == 1

    # Test 4: a two-row, two-column grid has one valid path.
    # assert count_paths(2, 2) == 1

    pass

# Question 7: Path Minimizing the Maximum Cell (Swim in Rising Water)
# MAIN QUESTION ONLY. Follow-ups come after both main-question passes.
#
# You are given an n x n grid of elevations. Water rises over time. At time t,
# you may stand on cells whose elevation is at most t and move up, down, left,
# or right between reachable cells. Return the minimum time needed to reach the
# bottom-right cell from the top-left cell.
#
# Example 1:
# grid = [[0, 2], [1, 3]]
# Expected result: 3
# The destination cannot be reached until the water level reaches elevation 3.
#
# Example 2:
# grid = [
#     [0, 1, 2, 3, 4],
#     [24, 23, 22, 21, 5],
#     [12, 13, 14, 15, 16],
#     [11, 17, 18, 19, 20],
#     [10, 9, 8, 7, 6],
# ]
# Expected result: 16
# The route reaches the destination when the largest elevation on the best
# route is 16.
#
# Constraints from the question:
# - The grid is n x n.
# - 1 <= n <= 50.
# - Elevations are unique integers from 0 through n*n - 1.


def swim_in_water(grid):
    # TODO: Build the main solution with guided questions.
    pass


if __name__ == "__main__":
    # Test 1: the first PDF example.
    # grid = [[0, 2], [1, 3]]
    # assert swim_in_water(grid) == 3

    # Test 2: the second PDF example.
    # grid = [
    #     [0, 1, 2, 3, 4],
    #     [24, 23, 22, 21, 5],
    #     [12, 13, 14, 15, 16],
    #     [11, 17, 18, 19, 20],
    #     [10, 9, 8, 7, 6],
    # ]
    # assert swim_in_water(grid) == 16

    # Test 3: a one-cell grid is already at the destination.
    # assert swim_in_water([[7]]) == 7

    # Test 4: a simple increasing route.
    # assert swim_in_water([[0, 1], [2, 3]]) == 3

    pass

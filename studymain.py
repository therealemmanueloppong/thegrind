# =====================================================================
# QUESTION 2: Infection Spread on a Grid (Cellular Automaton)
# CURRENT PRACTICE QUESTION
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
    # TODO: Write your solution here, one guided step at a time.
    pass


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

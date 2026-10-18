"""Day 2 - October 17, 2026: four Medium questions from the Stack section.

Source: All Questions - 2 column (Medium, Hard, Easy).pdf
Today's tracker questions: PDF Q50-53. Skeletons only; write your own code.
Day 1 Q46-49 are completed and commented in the720.py.
"""

from __future__ import annotations


# Shared node definitions; BSTIterator uses TreeNode.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# -----------------------------------------------------------------------------
# PDF Q50 | LeetCode 155 | Min Stack | Medium | source page 119
# -----------------------------------------------------------------------------
class MinStack:
    """Support push, pop, top, and getMin, each in O(1) time.

    pop, top, and getMin are called only when the stack is nonempty.
    """

    def __init__(self):
        """Initialize the object."""
        pass

    def push(self, val: int) -> None:
        """Add val to the top."""
        pass

    def pop(self) -> None:
        """Remove the top element."""
        pass

    def top(self) -> int:
        """Return the top element."""
        pass

    def getMin(self) -> int:
        """Return the minimum element currently present."""
        pass


# Your Q50 tests: add after implementing the methods; fill expected results yourself.


# -----------------------------------------------------------------------------
# PDF Q51 | LeetCode 173 | Binary Search Tree Iterator | Medium | source page 121
# -----------------------------------------------------------------------------
class BSTIterator:
    """Iterate over the in-order traversal of a binary search tree.

    The first next() returns the smallest value. Calls to next() are valid.
    Follow-up: average O(1) time for next/hasNext and O(h) memory,
    where h is the tree height.
    """

    def __init__(self, root: TreeNode | None):
        """Initialize an iterator positioned before the first value."""
        pass

    def next(self) -> int:
        """Advance and return the next value."""
        pass

    def hasNext(self) -> bool:
        """Return whether another value remains."""
        pass


# Your Q51 tests: add after implementing the methods; fill expected results yourself.


# -----------------------------------------------------------------------------
# PDF Q52 | LeetCode 227 | Basic Calculator II | Medium | source page 123
# -----------------------------------------------------------------------------
class BasicCalculatorIISolution:
    def calculate(self, s: str) -> int:
        """Evaluate a valid expression with nonnegative integers, spaces, and + - * /.

        Integer division truncates toward zero. Do not use eval() or another
        built-in function that evaluates mathematical expression strings.

        Examples from the PDF:
            '3+2*2' -> 7
            ' 3/2 ' -> 1
            ' 3+5 / 2 ' -> 5
        """
        pass


# Your Q52 tests: add after implementing the method; fill expected results yourself.


# -----------------------------------------------------------------------------
# PDF Q53 | LeetCode 255 | Verify Preorder Sequence in Binary Search Tree | Medium
# Source page 125
# -----------------------------------------------------------------------------
class VerifyPreorderBSTSolution:
    def verifyPreorder(self, preorder: list[int]) -> bool:
        """Return whether these unique integers can be the preorder of a BST.

        Examples from the PDF:
            [5, 2, 1, 3, 6] -> True
            [5, 2, 6, 1, 3] -> False

        Follow-up: use only constant extra space.
        """
        pass


# Your Q53 tests: add after implementing the method; fill expected results yourself.

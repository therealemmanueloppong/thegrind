print("the grind 720")


# =============================================================================
# Completed Day 1 question: user implementation, tests, and PDF comparison.
# PDF Q46 | LeetCode 71 | Simplify Path | Medium
# -----------------------------------------------------------------------------
class SimplifyPathSolution:
    def simplifyPath(self, path: str) -> str:
        """Return the canonical form of an absolute Unix path.

        A single dot means the current directory; two dots mean the parent.
        Repeated slashes count as one. Names such as '...' are ordinary names.
        The result starts with '/', with no trailing slash unless it is '/'.

        Examples from the PDF:
            '/home/' -> '/home'
            '/home/user/Documents/../Pictures' -> '/home/user/Pictures'
        """
        # Break the path at slashes; repeated or boundary slashes create empty parts.
        paths =  path.split('/')
        # Keep the folder names that remain in the simplified path, in order.
        stack = []

        # Read each path component from left to right.
        for p in paths:
            # A parent-directory marker cancels the most recently kept folder.
            if p == '..':
                # Only remove a folder when one exists; root has no parent to remove.
                if stack:
                    # Remove the last folder name, moving one level toward root.
                    stack.pop()

            # Empty parts come from extra slashes; a single dot means stay where we are.
            elif not p or p == '.':
                # Neither case changes the kept folders, so move to the next part.
                continue

            # All other components, including three dots, are ordinary names.
            else:
                # Keep this folder as the new final folder in the path.
                stack.append(p)


        # Every absolute canonical path must begin at root with one slash.
        base = '/'
        # Put exactly one slash between the remaining folder names.
        fullp = '/'.join(stack)
        # Add the leading slash; an empty folder list naturally produces root alone.
        return base + fullp


# Your Q46 tests: write two or three after implementing the method.

# Test 1: repeated slashes and a trailing slash.
assert SimplifyPathSolution().simplifyPath('/home//foo/') == '/home/foo'

# Test 2: '..' goes up from Documents to user, then enters Pictures.
assert SimplifyPathSolution().simplifyPath('/home/user/Documents/../Pictures') == '/home/user/Pictures'

# Test 3: trying to go above root.
assert SimplifyPathSolution().simplifyPath('/../') == '/'



# Comparison solution: same stack approach as the source PDF, pages 111-112.
# Both versions take O(n) time and O(n) space, where n is len(path).
# This version combines the skip conditions and builds the return string directly.
class SimplifyPathComparisonSolution:
    def simplifyPath(self, path: str) -> str:
        # Remember the surviving folder names; the end represents the current folder.
        stack = []
        # Separate the path into components and process them in their original order.
        for component in path.split('/'):
            # Going to the parent means undoing the latest stored folder.
            if component == '..':
                # At root the stack is empty, so there is no folder to undo.
                if stack:
                    # Discard the last surviving folder name.
                    stack.pop()
            # Keep only ordinary names; empty strings and a single dot are ignored.
            elif component and component != '.':
                # Extend the surviving path by one folder.
                stack.append(component)
        # Build the same canonical string directly; an empty stack gives one slash.
        return '/' + '/'.join(stack)


# The same three checks for the comparison implementation.
assert SimplifyPathComparisonSolution().simplifyPath('/home//foo/') == '/home/foo'
assert SimplifyPathComparisonSolution().simplifyPath('/home/user/Documents/../Pictures') == '/home/user/Pictures'
assert SimplifyPathComparisonSolution().simplifyPath('/../') == '/'

# Shared node definition used by archived tree questions.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        # Store this tree node's value; flattening must keep the same node objects.
        self.val = val
        # Remember the left child, or None if that branch is absent.
        self.left = left
        # Remember the right child; after flattening this link leads to the next node.
        self.right = right


# =============================================================================
# Completed Day 1 question: user implementation, tests, and PDF comparison.
# -----------------------------------------------------------------------------
# PDF Q47 | LeetCode 114 | Flatten Binary Tree to Linked List | Medium
# -----------------------------------------------------------------------------
class FlattenTreeSolution:
    def flatten(self, root: TreeNode | None) -> None:
        """Modify the tree in place into a chain in preorder traversal order.

        Use the existing TreeNode objects. Every left pointer becomes None;
        right pointers connect the nodes in the resulting chain.
        This method does not return a new tree.

        Example from the PDF (tree input is shown in level order):
            root = [1, 2, 5, 3, 4, None, 6]
            right-pointer chain: 1 -> 2 -> 3 -> 4 -> 5 -> 6
            every left pointer: None
        """
        # An empty tree has no nodes or links to rearrange.
        if not root:
            # Stop without creating or returning a different tree.
            return None

        #preorder
        # The root is the first node waiting for a preorder visit.
        stack = [root]
        # No node has been visited yet, so there is no previous chain node.
        prev = None
        # Keep visiting until there are no waiting nodes left.
        while stack:
            # Take the most recently stored node as the next visit.
            curr = stack.pop()
            # This version can push missing children; detect those None entries here.
            if not curr:
                # Skip a missing child before trying to read its links or update prev.
                continue
            # Only connect a predecessor after a real earlier node has been visited.
            if prev:
                # Append the current visit to the chain by changing the previous right link.
                prev.right = curr
                # Erase the previous node's old left branch so the result is a right-only chain.
                prev.left = None
            # Remember this real node for the next visit; keep this OUTSIDE the if prev guard.
            prev = curr
            # Save the right child first, so it waits underneath the left child.
            stack.append(curr.right)
            # Save the left child last, so the next pop visits it before the right side.
            stack.append(curr.left)





# Your Q47 tests: write two or three after implementing the method.

# Test 1: empty tree. Fill in the expected result after ==.
assert FlattenTreeSolution().flatten(None) == None

# Test 2: one node. Fill in the expected (value, left pointer, right pointer).
q47_single = TreeNode(0)
FlattenTreeSolution().flatten(q47_single)
assert (q47_single.val, q47_single.left, q47_single.right) == (0,None,None)


# Test 3: the branching tree from the PDF. Fill in the expected node values.
#         1
#        / \
#       2   5
#      / \   \
#     3   4   6
q47_nodes = [TreeNode(value) for value in (1, 2, 5, 3, 4, 6)]
q47_n1, q47_n2, q47_n5, q47_n3, q47_n4, q47_n6 = q47_nodes
q47_n1.left, q47_n1.right = q47_n2, q47_n5
q47_n2.left, q47_n2.right = q47_n3, q47_n4
q47_n5.right = q47_n6
FlattenTreeSolution().flatten(q47_n1)

# Follow right pointers; check for cycles and unwanted left branches.
q47_chain = []
q47_seen = set()
q47_cursor = q47_n1
while q47_cursor is not None:
    assert id(q47_cursor) not in q47_seen, 'The chain contains a cycle.'
    q47_seen.add(id(q47_cursor))
    assert q47_cursor.left is None, 'A left pointer was not cleared.'
    q47_chain.append(q47_cursor.val)
    q47_cursor = q47_cursor.right

# Check that every original node was reused, with no nodes lost or added.
assert q47_seen == {id(node) for node in q47_nodes}
assert q47_chain == [1,2,3,4,5,6]


# Comparison solution: pointer-rewiring approach from the current PDF, page 113.
# User version: O(n) time, O(h) extra stack space, up to O(n) in the worst case.
# Comparison: O(n) time, O(1) extra space. Both reuse the original nodes.
class FlattenTreeComparisonSolution:
    def flatten(self, root: TreeNode | None) -> None:
        # Walk through the tree using pointers rather than a separate stack.
        current = root
        # Process real nodes until the rightward walk reaches the end.
        while current:
            # A left subtree must be moved into the rightward visit path.
            if current.left:
                # Begin searching along the right edge of the left subtree.
                rightmost = current.left
                # Follow existing right links to find where to attach the old right subtree.
                while rightmost.right:
                    # Advance along that right edge without allocating another node.
                    rightmost = rightmost.right
                # Preserve the old right subtree by attaching it after the left-side path.
                rightmost.right = current.right
                # Put the left subtree next in the rightward chain, preserving preorder.
                current.right = current.left
                # Clear the old left link now that the subtree is reachable on the right.
                current.left = None
            # Continue with the next node on the evolving right-only path.
            current = current.right


# Verify the comparison with fresh copies of the same three cases.
def _q47_check_comparison():
    solution = FlattenTreeComparisonSolution()
    assert solution.flatten(None) is None
    single = TreeNode(0)
    solution.flatten(single)
    assert (single.val, single.left, single.right) == (0, None, None)

    nodes = [TreeNode(value) for value in (1, 2, 5, 3, 4, 6)]
    n1, n2, n5, n3, n4, n6 = nodes
    n1.left, n1.right = n2, n5
    n2.left, n2.right = n3, n4
    n5.right = n6
    solution.flatten(n1)
    chain, seen = [], set()
    cursor = n1
    while cursor is not None:
        assert id(cursor) not in seen, 'The comparison created a cycle.'
        seen.add(id(cursor))
        assert cursor.left is None, 'The comparison left a left pointer.'
        chain.append(cursor.val)
        cursor = cursor.right
    assert seen == {id(node) for node in nodes}
    assert chain == [1, 2, 3, 4, 5, 6]


_q47_check_comparison()

# Shared node definition used by archived linked-list questions.
class ListNode:
    def __init__(self, val=0, next=None):
        # Store the node's value; reordering must not change this value.
        self.val = val
        # Remember the next node, or None to mark the end of the list.
        self.next = next


# =============================================================================
# Completed Day 1 question: user implementation, tests, and PDF comparison.
# -----------------------------------------------------------------------------
# PDF Q48 | LeetCode 143 | Reorder List | Medium
# -----------------------------------------------------------------------------
class ReorderListSolution:
    def reorderList(self, head: ListNode | None) -> None:
        """Reorder the existing linked-list nodes in place.

        Required order: L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
        Do not change node values. This method does not return a new list.

        Examples from the PDF:
            1 -> 2 -> 3 -> 4       becomes 1 -> 4 -> 2 -> 3
            1 -> 2 -> 3 -> 4 -> 5  becomes 1 -> 5 -> 2 -> 4 -> 3
        """
        # An empty list or a single node is already in its required order.
        if not head or not head.next:
            # Leave the list unchanged and return no node; the caller still keeps head.
            return  None

        # Store references to every original node so back nodes can be taken with pop.
        stack = []
        # Start the collection walk at the first node without moving the caller's head.
        curr = head
        # Collect nodes until the walk has passed the original tail.
        while curr:
            # Store the node itself, not just its value, because we must reconnect original nodes.
            stack.append(curr)
            # Advance the collection walk; this eventually makes curr None and ends this loop.
            curr = curr.next

        # AFTER the collection loop, reset the walking reference to the front of the list.
        curr = head
        # Form one front/back pair per iteration; an odd middle node is left for the end.
        for i in range(len(stack)//2):
            # Take the next unused node from the original back of the list.
            lastnode = stack.pop()
            # SAVE the original next front node BEFORE overwriting curr.next.
            nextnode = curr.next
            # Connect the current front node to the selected back node.
            curr.next = lastnode
            # Reconnect that back node to the saved front remainder.
            lastnode.next = nextnode
            # Advance the front reference to the saved node for the next pair.
            curr = nextnode

        # AFTER the whole for loop, cut the final old link to prevent a cycle or self-link.
        curr.next = None


# Your Q48 tests: write two or three after implementing the method.
# Order reminder: first -> last -> second -> second-last -> third -> third-last -> ...
# For 1 -> 2 -> 3 -> 4 -> 5, the order is 1 -> 5 -> 2 -> 4 -> 3.


# Test 1: four-node input from the PDF: 1 -> 2 -> 3 -> 4.
q48_nodes = [ListNode(value) for value in (1, 2, 3, 4)]
for q48_left, q48_right in zip(q48_nodes, q48_nodes[1:]):
    q48_left.next = q48_right
ReorderListSolution().reorderList(q48_nodes[0])

# Read the changed list and check that every original node appears once.
q48_result = []
q48_seen = set()
q48_cursor = q48_nodes[0]
while q48_cursor is not None:
    assert id(q48_cursor) not in q48_seen, 'The reordered list contains a cycle.'
    q48_seen.add(id(q48_cursor))
    q48_result.append(q48_cursor.val)
    q48_cursor = q48_cursor.next
assert q48_seen == {id(node) for node in q48_nodes}
assert [node.val for node in q48_nodes] == [1, 2, 3, 4], 'Node values must not change.'

# Fill in the expected list of values after ==, using square brackets.
assert q48_result == [1,4,2,3]


# Test 2: five-node input from the PDF: 1 -> 2 -> 3 -> 4 -> 5.
q48_odd_nodes = [ListNode(value) for value in (1, 2, 3, 4, 5)]
for q48_left, q48_right in zip(q48_odd_nodes, q48_odd_nodes[1:]):
    q48_left.next = q48_right
ReorderListSolution().reorderList(q48_odd_nodes[0])

q48_odd_result = []
q48_odd_seen = set()
q48_cursor = q48_odd_nodes[0]
while q48_cursor is not None:
    assert id(q48_cursor) not in q48_odd_seen, 'The five-node result contains a cycle.'
    q48_odd_seen.add(id(q48_cursor))
    q48_odd_result.append(q48_cursor.val)
    q48_cursor = q48_cursor.next
assert q48_odd_seen == {id(node) for node in q48_odd_nodes}
assert [node.val for node in q48_odd_nodes] == [1, 2, 3, 4, 5], 'Node values must not change.'

# Fill in the expected list after ==, using square brackets.
assert q48_odd_result == [1,5,2,4,3]


# Test 3: single-node input: 7 -> None.
q48_single = ListNode(7)
ReorderListSolution().reorderList(q48_single)
assert q48_single.next is None, 'A single node must still have no next node.'
q48_single_result = [q48_single.val]
# Fill in the expected list after ==, using square brackets.
assert q48_single_result == [7]


# Comparison: adapted from the current PDF, pages 115-116.
# Both approaches take O(n) time. Your stack uses O(n) extra space;
# this version uses O(1) extra space: find the middle, reverse, then weave.
class ReorderListComparisonSolution:
    def reorderList(self, head: ListNode | None) -> None:
        # Nothing needs rearranging when fewer than two nodes exist.
        if not head or not head.next:
            # Finish without returning or replacing the caller's head node.
            return

        # Start two walkers together to locate the middle without storing all nodes.
        slow = fast = head
        # Continue while the faster walker can advance; the slower one approaches the middle.
        while fast and fast.next:
            # Move the slow walker one node per iteration.
            slow = slow.next
            # Move the fast walker two nodes per iteration.
            fast = fast.next.next

        # Prepare to reverse the portion beginning at the middle node.
        previous, current = None, slow
        # Reverse each node in that back portion exactly once.
        while current:
            # SAVE the next node before reversing the current link.
            following = current.next
            # Turn this next pointer backward toward the already reversed portion.
            current.next = previous
            # Extend the reversed portion and advance; the right-hand values are read first.
            previous, current = current, following

        # The two parts share the middle node; stop before linking it twice.
        # Start one walk at the original front and the other at the reversed back.
        first, second = head, previous
        # The halves share the middle node; stop when the back walker reaches that shared endpoint.
        while second.next:
            # SAVE both continuation links before changing either connection.
            next_first, next_second = first.next, second.next
            # Place the next back node immediately after the current front node.
            first.next = second
            # Connect that inserted node to the saved front continuation.
            second.next = next_first
            # Advance both walks to form the next front/back pair.
            first, second = next_first, next_second


# Check the comparison on fresh copies of the same three test cases.
def _q48_check_comparison():
    for input_values, expected_values in (
        ([1, 2, 3, 4], [1, 4, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
        ([7], [7]),
    ):
        nodes = [ListNode(value) for value in input_values]
        for left, right in zip(nodes, nodes[1:]):
            left.next = right
        ReorderListComparisonSolution().reorderList(nodes[0])
        result, seen = [], set()
        cursor = nodes[0]
        while cursor is not None:
            assert id(cursor) not in seen, 'The comparison created a cycle.'
            seen.add(id(cursor))
            result.append(cursor.val)
            cursor = cursor.next
        assert seen == {id(node) for node in nodes}
        assert [node.val for node in nodes] == input_values
        assert result == expected_values


_q48_check_comparison()

# =============================================================================
# Completed Day 1 question: user implementation, tests, and PDF comparison.
# -----------------------------------------------------------------------------
# PDF Q49 | LeetCode 150 | Evaluate Reverse Polish Notation | Medium
# -----------------------------------------------------------------------------
class ReversePolishNotationSolution:
    def evalRPN(self, tokens: list[str]) -> int:
        """Evaluate a valid expression written with operands before operators.

        Operators are '+', '-', '*', and '/'. Division truncates toward zero.
        The input is valid and never requires division by zero.

        Examples from the PDF:
            ['2', '1', '+', '3', '*'] -> 9   ((2 + 1) * 3)
            ['4', '13', '5', '/', '+'] -> 6 (4 + (13 / 5))
        """
        # Keep numbers and completed subexpression results that are waiting for another operation.
        stack = []
        
        # Read whole string items from left to right, including multi-digit and negative numbers.
        for c in tokens:
            # A sign consumes two waiting values; a valid input guarantees they exist.
            if c in '+-*/':
                # Pop the more recent value FIRST: it is the RIGHT side of subtraction or division.
                b = stack.pop()
                # Pop the earlier value SECOND: it is the LEFT side, so the operation is a op b.
                a = stack.pop()

                # Only the branch matching this sign will run; the separate checks are mutually exclusive.
                if c== '+':
                    # Put the sum back so a later sign can use it as one value.
                    stack.append(a+b)

                # Subtraction needs the original left-to-right operand order.
                if c== '-':
                    # Subtract the later value from the earlier one, then keep the result.
                    stack.append(a-b)


                # Recognize multiplication separately from addition.
                if c== '*':
                    # Multiply the two popped values and keep their product.
                    stack.append(a*b)

                # Division also uses a divided by b, rather than reversing the popped values.
                if c== '/':
                    # Convert the quotient to int to discard its fraction toward zero, including negative results.
                    stack.append(int(a/b))

            # This belongs to the OUTER sign check and handles complete number strings.
            else:
                # Convert this entire item once and store it separately; do not combine different items into digits.
                stack.append(int(c))


        # AFTER the for loop, return the one final integer; a zero answer still occupies one stack entry.
        return stack[0]




# Your Q49 tests: write two or three after implementing the method.

# Test 1: zero result. Fill in the expected integer after ==.
assert ReversePolishNotationSolution().evalRPN(["5", "5", "-"]) == 0

# Test 2: mixed operations from our practice example (not a PDF example).
assert ReversePolishNotationSolution().evalRPN(["8", "3", "2", "*", "-", "4", "+", "2", "/"]) == 3

# Test 3: negative division. Discard the fractional part toward zero.
# Fill in the expected integer after ==.
assert ReversePolishNotationSolution().evalRPN(["7", "-3", "/"]) == -2

# Comparison solution: operator lookup from the current PDF, page 118.
# Both versions use O(n) time and O(n) extra space. The mapping groups the
# operations in one place; the stack order and arithmetic are unchanged.
class ReversePolishNotationComparisonSolution:
    def evalRPN(self, tokens: list[str]) -> int:
        # Remember values waiting to be used, exactly as in the user's stack approach.
        stack = []
        # Associate each sign with a small function that accepts the earlier a and later b.
        ops = {
            # Addition combines the two values into their sum.
            '+': lambda a, b: a + b,
            # Keep operand order: earlier value minus later value.
            '-': lambda a, b: a - b,
            # Multiplication combines the two values into their product.
            '*': lambda a, b: a * b,
            # Use a divided by b and drop the fraction toward zero, rather than floor toward negative infinity.
            '/': lambda a, b: int(a / b),
        }
        # Read each complete input item in its original order.
        for token in tokens:
            # Look up whether this item names one of the supported operations.
            if token in ops:
                # Python evaluates these pops left to right: b gets the newer value, then a gets the older one.
                b, a = stack.pop(), stack.pop()
                # Select the function, pass the earlier value then the later value, and keep its result.
                stack.append(ops[token](a, b))
            # An item not naming an operation is a complete integer string.
            else:
                # Convert and store that number, including a leading minus sign when present.
                stack.append(int(token))
        # Valid input ends with exactly one waiting value; return that integer after the loop.
        return stack[0]


# The same three checks for the comparison implementation.
assert ReversePolishNotationComparisonSolution().evalRPN(["5", "5", "-"]) == 0
assert ReversePolishNotationComparisonSolution().evalRPN(["8", "3", "2", "*", "-", "4", "+", "2", "/"]) == 3
assert ReversePolishNotationComparisonSolution().evalRPN(["7", "-3", "/"]) == -2

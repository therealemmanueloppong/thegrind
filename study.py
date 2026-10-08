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

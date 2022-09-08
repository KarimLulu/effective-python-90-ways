def closestValue(root, target: float) -> int:
    # traverse
    # iterative traversal
    stack = []
    prev = float("-inf")
    while root or stack:
        # go to the left
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        if prev <= target and target <= root.val:
            return prev if abs(prev - target) <= abs(target - root.val) else root.val
        prev = root.val
        root = root.right
    return prev


class Node:
    def __init__(self, data=None, left=None, right=None):
        self.val = data
        self.left = left
        self.right = right
root = Node(2)
root.left = Node(1)
root.right = Node(3)
print(closestValue(root, 0.142857))

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(val={self.val}, right={self.right}, left={self.left})"


def increasingBST(root: TreeNode) -> TreeNode:
    def traverse(root):
        nonlocal cur
        if root is not None:
            traverse(root.left)
            cur.right = root
            root.left = None
            cur = root
            traverse(root.right)
    ans = cur = TreeNode(None)
    traverse(root)
    return ans.right




root = [5,3,6,2,4,None,8,1,None,None,None,None, None,7,9]
i_to_node = {}
for i, val in enumerate(root):
    if val is not None:
        node = TreeNode(val=val)
        i_to_node[i] = node
        parent = (i - 1) // 2
        if parent in i_to_node:
            left = (2 * parent + 1) == i
            if left:
                i_to_node[parent].left = node
            else:
                i_to_node[parent].right = node

root = i_to_node[0]
print(increasingBST(root))

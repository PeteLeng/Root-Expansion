import math
import random


class TreeNode:
    def __init__(self, val=None) -> None:
        self.val = val
        self.left = None
        self.right = None

class BSTreeNode(TreeNode):
    def __init__(self, val=None) -> None:
        super().__init__(val)
        self.parent = None
        self.lwid = 0
        self.rwid = 0
        self.pos = (0, 0)

    def insert(self, node):
        # Iterative
        # parent = self
        # while True:
        #     if node.val <= parent.val:
        #         if parent.left is None:
        #             parent.left = node
        #         else:
        #             parent = parent.left
        #             continue
        #     else:
        #         if parent.right is None:
        #             parent.right = node
        #         else:
        #             parent = parent.right
        #             continue

        # Recursive
        if node.val <= self.val:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert(node)

    def find(self, val):
        if val == self.val:
            return self
        if val < self.val:
            if self.left is None:
                print(f"{val} not found in tree")
                return None
            else:
                self.left.find(val)
        if val > self.val:
            if self.right is None:
                print(f"{val} not found in tree")
                return None
            else:
                self.right.find(val)

    def get_min(self):
        node = self
        while node.left is not None:
            node = node.left
        print(f"min val in tree: {node.val}")
        return node

    def get_max(self):
        node = self
        while node.right is not None:
            node = node.right
        print(f"max val in tree: {node.val}")
        return node

    def get_predecessor(self):
        if self.left is not None:
            return self.left.get_max()
        if self.parent is not None and self.parent.val < self.val:
            return self.parent
        else:
            print(f"{self.val} is the smallest value in tree")
            return None

    def get_successor(self):
        if self.right is not None:
            return self.right.get_min()
        if self.parent is not None and self.parent.val >= self.val:
            return self.parent
        else:
            print(f"{self.val} is the largest value in tree")
            return None

    def traverse(self):
        q = [self]
        while q:
            node = q.pop(0)
            if node is None:
                continue
            yield node
            q = [node.left, node.right] + q
            # print([n.val if n is not None else None for n in q])

    def annotate(self, f):
        if self.left is not None:
            self.left.annotate(f)
        if self.right is not None:
            self.right.annotate(f)
        f(self)

    def serialize(self):
        # Provide a string representation for the contents of the tree:
        # If I want to align nodes of same depth and the branches at the same time,
        # it will waste too much space.
        # The more efficient option is to only align branches at an arbitray angle, say 45.
        # A few observations:
        # - if the right tree is over half the height of the left tree
        #   its left child need not worry about collision
        # Naive solution:
        # - One pass of DFS search to annotate all nodes with subtree information
        #   and store the left-subtree, right-subtree width in self.ser_para
        def cal_wid(node):
            node.lwid = 0 if node.left is None else \
                node.left.lwid \
                + max(node.left.rwid, len(str(node.left.val)) + 1)
            node.rwid = 0 if node.right is None else \
                node.right.rwid \
                + max(node.right.lwid, len(str(node.right.val)) + 1)

        self.annotate(cal_wid)
            
        for node in self.traverse():

            pnode = node.parent
            if pnode is None:
                node.pos = (0, 0)
            else:
                px, py = pnode.pos
                wid = len(str(node.val))
                if node.val <= pnode.val:
                    delta = max(wid + 1, node.rwid) - 1
                    node.pos = (px - delta, py + delta)
                if node.val > node.parent.val:
                    delta = max(wid + 1, node.lwid) - 1
                    node.pos = (px + delta, py + delta)
        for node in self.traverse(): 
            # print(f"{node.val}: ({node.lwid}, {node.rwid})")
            print(f"{node.val}: {node.pos}")


def print_tree(rnode: BSTreeNode):
    xmin = xmax = ymin = ymax = 0
    
    def cal_dimension(node):
        x, y = node.pos
        nonlocal xmin, xmax, ymin, ymax
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
        
    rnode.annotate(cal_dimension)
    print(f"x: [{xmin}, {xmax}]\ny: [{ymin}, {ymax}]")

    row, col = ymax - ymin + 1, xmax - xmin + 1
    res = [["-" for _ in range(col + 1)] for _ in range(row)]
    for i in range(row):
         res[i][col] = "\n"

    def draw_node(node: BSTreeNode):
        nonlocal res, xmin
        x, y = node.pos
        s = str(node.val)
        print(f"node {s}: ({x}, {y})")
        l = len(s)
        if node.parent is None:
            for i in range(l):
                res[y][x - xmin + i] = s[i]
        else:
            if node.val <= node.parent.val:
                for i in range(l):
                    res[y][x - xmin + i] = s[i]
            else:
                for i in range(l):
                    res[y][x - xmin - i] = s[l - 1 - i]

    def draw_edge(node: BSTreeNode):
        nonlocal res, xmin
        pnode = node.parent
        if pnode is None: return
        px, py = pnode.pos
        x, y = node.pos
        if node.val <= pnode.val:
            # node is to the left of the parent node
            for (i, j) in zip(range(px - xmin - 1, x - xmin, -1), range(py + 1, y)):
                res[j][i] = "/"
        else:
            # node is to the right of the parent node 
            for (i, j) in zip(range(px - xmin + 1, x - xmin), range(py + 1, y)):
                res[j][i] = "\\"

    rnode.annotate(draw_node)
    rnode.annotate(draw_edge)
    print("".join([res[i][j] for i in range(row) for j in range(col + 1)]))


def main():
    print("Mars will prevail!")
    random.seed(0)
    nums = [random.randrange(0, 1000) for i in range(40)]
    print(nums)
    root = BSTreeNode(500)
    for n in nums:
        root.insert(BSTreeNode(n))
    root.serialize()
    print_tree(root)

    # there's edge cases where the left child of the right tree
    # collides with the right child of the left tree
    # To recreate:
    # random.seed(0)
    # nums = [random.randrange(0, 1000) for i in range(40)]
    # root = BSTreeNode(500)


if __name__ == '__main__':
    main()


# class Tree(object):
#     "Generic tree node."
#     def __init__(self, name='root', children=None):
#         self.name = name
#         self.children = []
#         if children is not None:
#             for child in children:
#                 self.add_child(child)
#     def __repr__(self):
#         return self.name
#     def add_child(self, node):
#         assert isinstance(node, Tree)
#         self.children.append(node)

# class Tree:
#     def __init__(self, data):
#         self.children = []
#         self.data = data
#
# left = Tree("left")
# middle = Tree("middle")
# right = Tree("right")
# root = Tree("root")
# root.children = [left, middle, right]

# class Node:
#
#     def __init__(self, data):
#
#         self.left = None
#         self.right = None
#         self.data = data
#
#     def insert(self, data):
# # Compare the new value with the parent node
#         if self.data:
#             if data < self.data:
#                 if self.left is None:
#                     self.left = Node(data)
#                 else:
#                     self.left.insert(data)
#             elif data > self.data:
#                 if self.right is None:
#                     self.right = Node(data)
#                 else:
#                     self.right.insert(data)
#         else:
#             self.data = data
#
# # Print the tree
#     def PrintTree(self):
#         if self.left:
#             self.left.PrintTree()
#         print( self.data),
#         if self.right:
#             self.right.PrintTree()
#
# # Use the insert method to add nodes
# root = Node(12)
# root.insert(6)
# root.insert(14)
# root.insert(3)
#
# root.PrintTree()


# Надо взять список защит. По этому списку зациклить (for) линии. Линии будут перебираться, пока (while) есть списки
# нерассмотренные узлы. Линии будут перебираться, пока (while) не наступит условие (if) последней шины. Каждая итерация
# будет добавлять в список рассмотренные узлы.

# h = [7]
# l = h
# print('1', l)
# h.remove(h[0])
# print('2', l)


# a = {'a': []}
# print(a['a'])
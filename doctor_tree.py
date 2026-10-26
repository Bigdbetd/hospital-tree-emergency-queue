"""A binary reporting hierarchy, not a name-sorted binary search tree."""


class DoctorNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    def __init__(self):
        self.root = None

    def _find(self, node, name):
        """Search each subtree recursively, stopping when a match is found."""
        if node is None or node.name == name:
            return node
        return self._find(node.left, name) or self._find(node.right, name)

    def insert(self, parent_name, employee_name, side):
        """Return success; invalid requests leave the hierarchy unchanged."""
        if not isinstance(side, str) or side.lower() not in ('left', 'right'):
            print('Error: side must be left or right.')
            return False
        side = side.lower()
        if not isinstance(employee_name, str) or not employee_name.strip():
            print('Error: doctor name must be a nonempty string.')
            return False
        parent = self._find(self.root, parent_name)
        if parent is None:
            print(f'Error: parent {parent_name!r} does not exist.')
            return False
        if self._find(self.root, employee_name) is not None:
            print('Error: doctor names must be unique for parent lookup.')
            return False
        if getattr(parent, side) is not None:
            print(f'Error: the {side} report of {parent_name} is occupied.')
            return False
        setattr(parent, side, DoctorNode(employee_name))
        return True

    def _traverse(self, node, order, result):
        """Append into one output list to avoid repeated subtree copying."""
        if node is None:
            return
        if order == 'pre':
            result.append(node.name)
        self._traverse(node.left, order, result)
        if order == 'in':
            result.append(node.name)
        self._traverse(node.right, order, result)
        if order == 'post':
            result.append(node.name)

    def preorder(self, node):
        result = []
        self._traverse(node, 'pre', result)
        return result

    def inorder(self, node):
        result = []
        self._traverse(node, 'in', result)
        return result

    def postorder(self, node):
        result = []
        self._traverse(node, 'post', result)
        return result


if __name__ == '__main__':
    tree = DoctorTree()
    tree.root = DoctorNode('Dr. Croft')
    tree.insert('Dr. Croft', 'Dr. Goldsmith', 'right')
    tree.insert('Dr. Croft', 'Dr. Phan', 'left')
    tree.insert('Dr. Phan', 'Dr. Carson', 'right')
    tree.insert('Dr. Phan', 'Dr. Morgan', 'left')
    print('Preorder:', tree.preorder(tree.root))
    print('Inorder:', tree.inorder(tree.root))
    print('Postorder:', tree.postorder(tree.root))

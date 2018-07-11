class LogicalTree:
    def __init__(self):
        pass

    def is_leaf(self):
        return False


class LogicalTreeBranch(LogicalTree):
    def __init__(self, func, args):
        LogicalTree.__init__(self)
        self.func = func
        self.args = args


class LogicalTreeLeaf(LogicalTree):
    def __init__(self, content):
        LogicalTree.__init__(self)
        self.content = content

    def is_leaf(self):
        return True

from knowledge.logical_tree import LogicalTreeLeaf


class Concept:
    def __init__(self):
        self.lexical_form = None

    def get_lexical_form(self):
        return self.lexical_form

    def get_logical_form(self, input_string=None, reader=None):
        if input_string in [None, self.lexical_form]:
            return LogicalTreeLeaf(self)
        else:
            return None


class Category(Concept):
    def __init__(self):
        Concept.__init__(self)


class Thing(Concept):
    def __init__(self):
        Concept.__init__(self)


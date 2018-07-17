from knowledge.didnt_understand import DidntUnderstand


class Reasoner:
    def __init__(self):
        pass

    def take_move(self, logical_tree):
        resolution = self.resolve(logical_tree)
        return resolution if resolution else DidntUnderstand()

    def resolve(self, logical_tree):
        if logical_tree is None:
            return None
        if logical_tree.is_leaf():
            return logical_tree.content
        resolved_args = [self.resolve(a) for a in logical_tree.args]
        return logical_tree.func(*resolved_args)


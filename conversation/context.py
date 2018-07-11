class ContextElement:
    def __init__(self):
        pass

    @staticmethod
    def is_expectation():
        return False


class Expectation(ContextElement):
    def __init__(self, content):
        ContextElement.__init__(self)
        self.content = content

    @staticmethod
    def is_expectation():
        return True


class Proposition(ContextElement):
    def __init__(self):
        ContextElement.__init__(self)

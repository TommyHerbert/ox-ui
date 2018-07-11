from main.knowledge.concept import Thing


class Hello(Thing):
    def __init__(self):
        Thing.__init__(self)
        self.lexical_form = 'Hello'
from main.knowledge.concept import Category


class Song(Category):
    def __init__(self):
        Category.__init__(self)
        self.lexical_form = 'song'

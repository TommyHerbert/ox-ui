from knowledge.concept import Category
from conversation.context import Expectation


class Question(Category):
    def __init__(self):
        Category.__init__(self)

    def get_logical_form(self, input_string=None, reader=None):
        if None in [input_string, reader]:
            return None
        question_logic = self.get_question_logic(input_string, reader)
        return Expectation(question_logic) if question_logic else None

    def get_question_logic(self, input_string, reader):
        return None


from knowledge.didnt_understand import DidntUnderstand


class NaiveConversationStrategy:
    def __init__(self):
        pass

    @staticmethod
    def pop_move(context):
        for i in range(len(context)):
            element = context[i]
            if element.is_expectation():
                del context[i]
                return element.content
        return DidntUnderstand().get_logical_form()


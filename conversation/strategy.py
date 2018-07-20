from knowledge.didnt_understand import DidntUnderstand


class NaiveConversationStrategy:
    def __init__(self):
        pass

    @staticmethod
    def pop_move(context):
        if not context:
            return NaiveConversationStrategy._didnt_understand()
        for i in range(len(context)):
            element = context[i]
            if element.is_expectation():
                del context[i]
                return element.content
        return NaiveConversationStrategy._didnt_understand()

    @staticmethod
    def _didnt_understand():
        return DidntUnderstand().get_logical_form()


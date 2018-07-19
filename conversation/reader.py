class Reader:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def read_last_move(self, conversation):
        logical_form = self.parse(conversation.utterances[-1].text)
        if logical_form:
            conversation.context.append(logical_form)

    def parse(self, utterance):
        for category in self.knowledge_base.categories:
            logical_form = category.get_logical_form(utterance, self)
            if logical_form:
                return logical_form
        return None

    def get_relations(self):
        return self.knowledge_base.relations


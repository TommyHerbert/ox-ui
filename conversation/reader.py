class Reader:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def get_relations(self):
        return self.knowledge_base.relations


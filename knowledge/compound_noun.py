from functools import partial
from main.knowledge.logical_tree import LogicalTreeBranch
from main.knowledge.relation import has_lexical_form


class CompoundNoun:
    def __init__(self):
        pass

    def get_logical_form(self, input_string, reader):
        words = input_string.split()
        if len(words) != 2:
            return None
        category = reader.parse(words[1])
        return LogicalTreeBranch(partial(self.find_referents, words[0], reader), [category]) if category else None

    def find_referents(self, qualifier_string, reader, category):
        relations = reader.get_relations()
        instances = [r.arguments[0] for r in relations if r.relation_type == 'is_a' and r.arguments[1] == category]
        return [i for i in instances if self.is_related(i, qualifier_string, relations)]

    @staticmethod
    def is_related(obj, lexical_form, relations):
        relevant_relations = [r for r in relations if obj in r.arguments and has_lexical_form(r, lexical_form)]
        return len(relevant_relations) > 0

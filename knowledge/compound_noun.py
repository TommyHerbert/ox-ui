from functools import partial
from knowledge.logical_tree import LogicalTreeBranch
from knowledge.relation import has_lexical_form


class CompoundNoun:
    def __init__(self):
        pass

    def get_logical_form(self, input_string, reader):
        words = input_string.split()
        if len(words) != 2:
            return None
        category = reader.parse(words[1])
        if not category:
            return None
        find_referents = partial(self.find_referents, words[0], reader)
        return LogicalTreeBranch(find_referents, [category])

    def find_referents(self, qualifier_string, reader, category):
        def instance(r):
            return r.relation_type == 'is_a' and r.arguments[1] == category
        relations = reader.get_relations()
        instances = [r.arguments[0] for r in relations if instance(r)]
        related = lambda i: self.is_related(i, qualifier_string, relations)
        return [i for i in instances if related(i)]

    @staticmethod
    def is_related(obj, lexical_form, relations):
        def relevant(r):
            return obj in r.arguments and has_lexical_form(r, lexical_form)
        return len([r for r in relations if relevant(r)]) > 0


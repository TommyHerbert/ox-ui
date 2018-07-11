class Relation:
    def __init__(self, relation_type, arguments):
        self.relation_type = relation_type
        self.arguments = arguments


def has_lexical_form(relation, lexical_form):
    for argument in relation.arguments:
        try:
            if argument.get_lexical_form() == lexical_form:
                return True
        except AttributeError:
            return False
    return False


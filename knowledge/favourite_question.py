from knowledge.question import Question
import re
from functools import partial
from knowledge.myself import Myself
from knowledge.logical_tree import LogicalTreeBranch
from knowledge.question import Question


class FavouriteQuestion(Question):
    def __init__(self):
        Question.__init__(self)

    def get_question_logic(self, input_string, reader):
        category_string = self.get_category_string(input_string)
        if not category_string:
            return None
        category = reader.parse(category_string)
        favourite = partial(self.find_favourite, reader)
        return LogicalTreeBranch(favourite, [category])

    @staticmethod
    def get_category_string(input_string):
        match = re.match("What's your favourite (.+)\?", input_string)
        return match.group(1) if match else None

    def find_favourite(self, reader, category):
        relations = reader.get_relations()
        instances = category
        def relevant(r):
            return r.relation_type == 'is_a' and r.arguments[1] == category
        if type(instances) != list:
            instances = [r.arguments[0] for r in relations if relevant(r)]
        return self.find_favourite_in_list(relations, instances)

    def find_favourite_in_list(self, relations, candidates):
        def ox_likes_relation(r):
            return r.relation_type == 'likes' and \
                   r.arguments[0].__class__ == Myself and \
                   r.arguments[1] in candidates
        ox_likes = [r for r in relations if ox_likes_relation(r)]
        if len(ox_likes) == 0:
            return None
        return max(ox_likes, key=lambda r: r.arguments[2]).arguments[1]


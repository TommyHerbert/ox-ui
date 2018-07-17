from knowledge.singer import Singer
from knowledge.song import Song
from knowledge.compound_noun import CompoundNoun
from knowledge.favourite_question import FavouriteQuestion
from knowledge.myself import Myself
from knowledge.adele import Adele
from knowledge.hello import Hello
from knowledge.someone_like_you import SomeoneLikeYou
from knowledge.relation import Relation
from utils.case import headline_to_snake


class KnowledgeBase:
    def __init__(self):
        # initialise lists
        self.categories = []
        self.things = []
        self.relations = []

        # instantiate categories
        singer = Singer()
        song = Song()
        compound_noun = CompoundNoun()
        favourite_question = FavouriteQuestion()

        # instantiate things
        myself = Myself()
        adele = Adele()
        hello = Hello()
        someone_like_you = SomeoneLikeYou()

        # populate categories
        self.categories.append(singer)
        self.categories.append(song)
        self.categories.append(compound_noun)
        self.categories.append(favourite_question)

        # populate things
        self.things.append(myself)
        self.things.append(adele)
        self.things.append(hello)
        self.things.append(someone_like_you)

        # populate relations
        def add_relation(name, args):
            self.relations.append(Relation(name, args))
        add_relation('is_a', (adele, singer))
        add_relation('is_a', (hello, song))
        add_relation('is_a', (someone_like_you, song))
        add_relation('sang', (adele, hello))
        add_relation('sang', (adele, someone_like_you))
        add_relation('likes', (myself, hello, 1000))
        add_relation('likes', (myself, someone_like_you, 900))

    def write(self):
        imports = []
        for category in self.categories:
            template = 'from knowledge.{} import {}' # TODO get package name
            class_name = category.__class__.__name__
            module_name = headline_to_snake(class_name)
            imports.append(template.format(module_name, class_name))
        # TODO
        imports.append('from utils.case import headline_to_snake')
        # TODO


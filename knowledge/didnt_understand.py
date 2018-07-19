from knowledge.concept import Thing


# It's kind of a Thing. Maybe eventually, DidntUnderstand will be a
# Proposition and Proposition will be a Thing. But I don't have
# Propositions yet.
class DidntUnderstand(Thing):
    def __init__(self):
        Thing.__init__(self)
        self.lexical_form = "Sorry, I didn't understand that."


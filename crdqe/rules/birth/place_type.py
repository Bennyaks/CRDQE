from crdqe.rules.generic.text_rule import TextRule


class PlaceTypeRule(TextRule):

    FIELD = "place_type"

    def __init__(self, schema=None):
        super().__init__(schema)
from crdqe.rules.generic.text_rule import TextRule


class OccupationRule(TextRule):

    FIELD = "occupation"

    def __init__(self, schema=None):
        super().__init__(schema)
from crdqe.rules.generic.text_rule import TextRule


class NationalityRule(TextRule):

    FIELD = "nationality"

    def __init__(self, schema=None):
        super().__init__(schema)
        
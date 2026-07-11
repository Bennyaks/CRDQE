from crdqe.rules.generic.text_rule import TextRule


class MaritalStatusRule(TextRule):

    FIELD = "marital_status"

    def __init__(self, schema=None):
        super().__init__(schema)
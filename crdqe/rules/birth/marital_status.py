from crdqe.rules.generic.text_rule import TextRule


class MaritalStatusRule(TextRule):

    FIELD = "marital_status"

    TITLE = "Marital Status"

    REQUIRED = True
from crdqe.rules.generic.text_rule import TextRule


class NationalityRule(TextRule):

    FIELD = "nationality"
    TITLE = "Nationality"

    REQUIRED = True
        
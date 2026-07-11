"""
Birth Rule

Mother Age
"""

from crdqe.rules.generic.numeric_rule import NumericRule


class MotherAgeRule(NumericRule):

    FIELD = "mother_age"
    TITLE = "Mother Age"
    
"""
Loads rules based on detected dataset.
"""


class RuleLoader:

    @staticmethod
    def load(dataset, schema):

        if dataset.lower() == "birth":

            from crdqe.rules.birth.registry import RULES

            return [rule(schema) for rule in RULES]

        elif dataset.lower() == "death":

            from crdqe.rules.death.registry import RULES

            return [rule(schema) for rule in RULES]
        raise ValueError(f"Unknown dataset: {dataset}")
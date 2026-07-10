"""
===========================================================
Generic Numeric Rule

Validates numeric fields using limits defined
in the schema.
===========================================================
"""

import pandas as pd

from crdqe.core.base_rule import BaseRule


class NumericRule(BaseRule):

    FIELD = None

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        minimum = self.schema.minimum(self.FIELD)
        maximum = self.schema.maximum(self.FIELD)

        for index, value in df[self.FIELD].items():

            if self.is_missing(value):

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Missing {self.FIELD}"
                )
                continue

            try:

                number = float(value)

            except Exception:

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Invalid {self.FIELD}",
                    value
                )
                continue

            if minimum is not None and number < minimum:

                self.add_issue(
                    index,
                    self.FIELD,
                    f"{self.FIELD} below minimum",
                    value
                )

            elif maximum is not None and number > maximum:

                self.add_issue(
                    index,
                    self.FIELD,
                    f"{self.FIELD} above maximum",
                    value
                )

            else:

                df.at[index, self.FIELD] = number

        return df, self.get_issues()
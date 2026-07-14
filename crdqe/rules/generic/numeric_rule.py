"""
===========================================================
Generic Numeric Rule

Validates numeric fields using limits defined
in the schema.
===========================================================
"""

from dataclasses import field

import pandas as pd

from crdqe.core.base_rule import BaseRule


class NumericRule(BaseRule):

    FIELD = None

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        self.field_schema = self.field_schema()

        minimum = self.field_schema.get("minimum")
        maximum = self.field_schema.get("maximum")

        for index, row in df.iterrows():

            value = row[self.FIELD]

            if self.is_missing(value):

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Missing {self.TITLE}"
                )
                continue

            try:

                number = float(value)

            except Exception:

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Invalid {self.TITLE}"
                )
                continue

            if minimum is not None and number < minimum:

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Invalid {self.TITLE}"
                )

            elif maximum is not None and number > maximum:

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Invalid {self.TITLE}"
                )

            else:

                df.at[index, self.FIELD] = number

        return df, self.get_issues()
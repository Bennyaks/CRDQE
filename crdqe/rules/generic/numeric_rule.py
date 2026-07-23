"""
===========================================================
Generic Numeric Rule

Validates numeric fields using limits defined
in the schema.
===========================================================
"""

from dataclasses import field

import pandas as pd
import re

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

                self.add_issue(
                    row=row.name,
                    field=self.FIELD,
                    value=value,
                    issue=f"Missing {self.TITLE}"
                )
                continue

            try:

                cleaned = str(value).strip().lower()

                # Only Birth Weight needs unit stripping
                if self.FIELD == "birth_weight":

                    cleaned = cleaned.replace(",", "")

                    match = re.search(
                        r"\d+(?:\.\d+)?",
                        cleaned
                    )

                    if match:
                        cleaned = match.group(0)

                number = float(cleaned)

            except Exception:

                self.add_issue(
                    row=row.name,
                    field=self.FIELD,
                    value=value,
                    issue=f"Invalid {self.TITLE}"
                )
                continue

            if minimum is not None and number < minimum:

                self.add_issue(
                    row=row.name,
                    field=self.FIELD,
                    value=value,
                    issue=f"Invalid {self.TITLE}"
                )

            elif maximum is not None and number > maximum:

                self.add_issue(
                    row=row.name,
                    field=self.FIELD,
                    value=value,
                    issue=f"Invalid {self.TITLE}"
                )

            else:

                # Birth weight specific cleaning
                if self.FIELD == "birth_weight":

                    # Convert grams to kilograms
                    if number > 100:
                        number /= 1000

                    # Standardize to 1 decimal place
                    number = round(number, 1)

                df.at[index, self.FIELD] = number

        return df, self.get_issues()
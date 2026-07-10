"""
===========================================================
Generic Categorical Rule

Validates fields with predefined valid values.

Examples:
- Sex
- Marital Status
- Nationality
- Education
- Place Type
===========================================================
"""

from crdqe.core.base_rule import BaseRule


class CategoricalRule(BaseRule):

    FIELD = None

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        valid_values = self.schema.valid_values(self.FIELD)

        for index, value in df[self.FIELD].items():

            if self.is_missing(value):

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Missing {self.FIELD}"
                )

                continue

            cleaned = str(value).strip().lower()

            if cleaned in valid_values:

                df.at[index, self.FIELD] = valid_values[cleaned]

            else:

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Invalid {self.FIELD}",
                    value
                )

        return df, self.get_issues()
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

        field_schema = self.schema["source_columns"][self.FIELD]

        valid_values = field_schema.get("valid_values", {})

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

            cleaned = str(value).strip().lower()

            if cleaned in valid_values:
                df.at[index, self.FIELD] = valid_values[cleaned]
            else:
                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Invalid {self.TITLE}"
                )

        return df, self.get_issues()
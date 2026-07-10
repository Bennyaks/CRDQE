"""
===========================================================
Birth Rule

Field:
Date of Birth
===========================================================
"""

import pandas as pd

from crdqe.core.base_rule import BaseRule


class DateOfBirthRule(BaseRule):

    FIELD = "date_of_birth"

    def run(self, dataframe):

        df = dataframe.copy()

        issues = []

        df[self.FIELD] = pd.to_datetime(
            df[self.FIELD],
            errors="coerce",
            dayfirst=True
        )

        today = pd.Timestamp.today().normalize()

        for index, value in df[self.FIELD].items():

            if pd.isna(value):

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Missing Date of Birth",
                    "value": None
                })

            elif value > today:

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Future Date of Birth",
                    "value": value
                })

        return df, pd.DataFrame(issues)
"""
===========================================================
Birth Rule

Date Consistency
===========================================================
"""

import pandas as pd

from crdqe.rules.generic.cross_field_rule import CrossFieldRule


class DateConsistencyRule(CrossFieldRule):

    def validate(self, index, row):

        birth = pd.to_datetime(
    row["date_of_birth"],
    errors="coerce",
    dayfirst=True
)

        registration = pd.to_datetime(
            row["registration_date"],
            errors="coerce",
            dayfirst=True
        )

        if pd.isna(birth) or pd.isna(registration):
            return

        if registration < birth:
            self.add_issue(
                row=index,
                field="registration_date",
                issue="Registration before Birth",
                value=row["registration_date"]
            )
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

        birth = row["date_of_birth"]
        registration = row["registration_date"]

        if pd.isna(birth) or pd.isna(registration):
            return

        if registration < birth:

            self.add_issue(
                index,
                "registration_date",
                "Registration date is before Date of Birth"
            )
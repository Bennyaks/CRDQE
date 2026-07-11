import pandas as pd

from crdqe.rules.generic.cross_field_rule import CrossFieldRule


class DateConsistencyRule(CrossFieldRule):

    def validate(self, index, row):

        death = pd.to_datetime(
            row["date_of_death"],
            errors="coerce",
            dayfirst=True
        )

        registration = pd.to_datetime(
            row["registration_date"],
            errors="coerce",
            dayfirst=True
        )

        if pd.isna(death) or pd.isna(registration):
            return

        if registration < death:

            self.add_issue(
                row=index + 2,
                field="registration_date",
                issue="Registration date before death date",
                value=registration
            )
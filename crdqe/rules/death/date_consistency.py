import pandas as pd

from crdqe.rules.generic.cross_field_rule import CrossFieldRule


class DateConsistencyRule(CrossFieldRule):

    def validate(self, index, row):

        event_date = pd.to_datetime(
            row["date_of_death"],
            dayfirst=True,
            errors="coerce"
        )

        registration_date = pd.to_datetime(
            row["registration_date"],
            dayfirst=True,
            errors="coerce"
        )

        if pd.isna(event_date) or pd.isna(registration_date):
            return

        if registration_date < event_date:

            self.add_issues(
                issues=self.issues,
                row=row,
                field="registration_date",
                value=registration_date,
                message="Registration date before death date"
            )
            
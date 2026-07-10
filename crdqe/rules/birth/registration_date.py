import pandas as pd

from crdqe.core.base_rule import BaseRule


class RegistrationDateRule(BaseRule):

    FIELD = "registration_date"

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
                    "issue": "Missing Registration Date",
                    "value": None
                })

            elif value > today:

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Future Registration Date",
                    "value": value
                })

        return df, pd.DataFrame(issues)
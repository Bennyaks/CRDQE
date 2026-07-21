import pandas as pd

from crdqe.core.base_rule import BaseRule


class RegistrationDateRule(BaseRule):

    FIELD = "registration_date"

    def __init__(self, schema=None):
        super().__init__(schema)

    def run(self, dataframe):

        df = dataframe.copy()

        issues = []

        today = pd.Timestamp.today().normalize()

        for index, value in df[self.FIELD].items():
            # get the full row so we can access other fields like entry_number
            row = df.loc[index]

            parsed = pd.to_datetime(
                value,
                errors="coerce",
                dayfirst=True
            )

            if pd.isna(parsed):

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Missing Registration Date",
                    "value": value,
                    "entry_number": row.get("entry_number", None)
                })

                continue

            if parsed > today:

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Future Registration Date",
                    "value": value,
                    "entry_number": row.get("entry_number", None)
                })

                continue

            df.at[index, self.FIELD] = parsed.strftime("%d-%m-%Y")

        return df, pd.DataFrame(issues)
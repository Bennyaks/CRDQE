"""
===========================================================
Birth Rule

Field:
Status

Purpose:
Determine whether registration is Current or Late.
===========================================================
"""

import pandas as pd

from crdqe.core.base_rule import BaseRule


class StatusRule(BaseRule):

    def run(self, dataframe):

        df = dataframe.copy()

        issues = []

        df["status"] = None

        for index, row in df.iterrows():

            dob = row["date_of_birth"]
            reg = row["registration_date"]

            if pd.isna(dob) or pd.isna(reg):

                df.at[index, "status"] = None

                issues.append({
                    "row": index + 2,
                    "field": "status",
                    "issue": "Cannot determine status due to missing date(s)",
                    "value": None
                })

                continue

            days = (reg - dob).days

            if days <= 180:
                df.at[index, "status"] = "Current"
            else:
                df.at[index, "status"] = "Late"

        return df, pd.DataFrame(issues)
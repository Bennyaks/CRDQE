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
            dob = pd.to_datetime(
                row["date_of_birth"],
                errors="coerce",
                dayfirst=True
            )
            reg = pd.to_datetime(
                row["registration_date"],
                errors="coerce",
                dayfirst=True
            )
            if pd.isna(dob) or pd.isna(reg):
                continue
            days = (reg - dob).days
            if days <= 180:
                df.at[index, "status"] = "Current"
            else:
                df.at[index, "status"] = "Late"

        return df, pd.DataFrame(issues)
"""
===========================================================
Death Rule

Field:
Status

Purpose:
Calculate registration status and validate existing values.
===========================================================
"""

import pandas as pd

from crdqe.core.base_rule import BaseRule
from crdqe.utils.status_calculator import StatusCalculator
from crdqe.core.status_processor import StatusProcessor


class StatusRule(BaseRule):

    def run(self, dataframe):

        df = dataframe.copy()

        issues = []

        # Was there already a status column?
        has_original_status = "Status" in df.columns

        # Always create/update our internal status column
        if "status" not in df.columns:
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

            expected = StatusCalculator.calculate(dob, reg)

            if expected is None:
                continue
            

            # Save calculated value
            df.at[index, "status"] = expected
            place = str(row["place_type"]).strip().lower()

            if (
                expected == "Late"
                and "health" in place
            ):

                self.add_issue(
                    row=row.name,
                    field="Status",
                    value=expected,
                    issue=(
                        "Late registration recorded at a Health Facility. "
                        "Verify registration date format."
                    )
                )
                        

            # Validate existing Status column if present
            if has_original_status:

                existing = str(row["Status"]).strip()

                if existing and existing.lower() != expected.lower():

                    issues.append({
                        "row": index + 2,
                        "field": "Status",
                        "issue": "Incorrect Status",
                        "current_value": existing,
                        "expected_value": expected,
                        "entry_number": row.get("entry_number", None)
                    })
        if "Status" in df.columns:
            df.drop(columns=["Status"], inplace=True)

        df.rename(
            columns={"status": "Status"},
            inplace=True
        )

        return df, pd.DataFrame(issues)
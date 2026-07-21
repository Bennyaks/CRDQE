import re
import pandas as pd

from crdqe.core.base_rule import BaseRule


class IDNumberRule(BaseRule):

    FIELD = "id_number"
    TITLE = "ID Number"

    def run(self, dataframe):

        df = dataframe.copy()
        issues = []

        # Ensure column is string
        df[self.FIELD] = df[self.FIELD].astype(str)

        for index, value in df[self.FIELD].items():

            value = "" if pd.isna(value) else str(value).strip()

            # Remove Excel's trailing .0
            if value.endswith(".0"):
                value = value[:-2]

            # Empty / missing
            if value == "" or value.lower() == "nan":

                df.at[index, self.FIELD] = "Not stated"

                issues.append({
                    "row": index + 2,
                    "field": self.FIELD,
                    "issue": "Missing ID Number",
                    "value": "",
                    "entry_number": df.at[index, "entry_number"] if "entry_number" in df.columns else None
                })

                continue

            # Standardize
            if value.lower() == "not stated":

                df.at[index, self.FIELD] = "Not stated"
                continue

            # Remove internal spaces
            cleaned = value.replace(" ", "")

            # Valid Kenyan ID (digits only)
            if cleaned.isdigit():

                df.at[index, self.FIELD] = cleaned
                continue

            # Valid passport (letters and numbers)
            if re.fullmatch(r"[A-Za-z0-9]+", cleaned):

                df.at[index, self.FIELD] = cleaned.upper()
                continue

            # Invalid value
            issues.append({
                "row": index + 2,
                "field": self.FIELD,
                "issue": "Invalid ID/Passport Number",
                "value": value
                ,"entry_number": df.at[index, "entry_number"] if "entry_number" in df.columns else None
            })

            df.at[index, self.FIELD] = cleaned

        return df, pd.DataFrame(issues)
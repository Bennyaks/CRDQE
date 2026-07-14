"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Base Rule

Purpose:
Base class for all validation and cleaning rules.
===========================================================
"""

import pandas as pd


class BaseRule:

    def __init__(self, schema=None):

        self.schema = schema
        self.issues = []

    def add_issues(
        self,
        issues,
        row,
        field,
        value,
        message,
        severity="Error"
    ):
        """
        Add a standardized issue.
        """

        record = {
            "entry_number": row.get("entry_number", None),
            "field": field,
            "value": value,
            "issue": message,
            "severity": severity
        }

        issues.append(record)

    def is_missing(self, value):

        if pd.isna(value):
            return True

        if str(value).strip() == "":
            return True
        return False
    def field_schema(self):
        return self.schema["source_columns"].get(self.FIELD, {})

    def get_issues(self):

        return pd.DataFrame(self.issues)

    def run(self, dataframe):
        raise NotImplementedError
    
    def reset(self):
        """Reset issues before every run."""
        self.issues = []


    def start(self, dataframe):
        """Prepare a working dataframe."""
        self.reset()
        return dataframe.copy()
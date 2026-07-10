"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Base Rule

Purpose:
Base class for all validation and cleaning rules.
===========================================================
"""

from operator import index

import pandas as pd


class BaseRule:

    def __init__(self, schema=None):

        self.schema = schema
        self.issues = []

    def add_issue(self, row, field, issue, value=None, suggestion=None, severity=None):

        entry_number = row + 1
        self.issues.append({
            "entry_number": entry_number,
            "row": row,
            "field": field,
            "value": value,
            "rule": self.__class__.__name__,
            "issue": issue,
            "suggestion": suggestion,
            "severity": severity
        })

    def is_missing(self, value):

        if pd.isna(value):
            return True

        if str(value).strip() == "":
            return True

        return False

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
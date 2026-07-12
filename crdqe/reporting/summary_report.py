"""
===========================================================
Summary Report

Generates overall statistics after validation.
===========================================================
"""

import pandas as pd


class SummaryReport:

    def __init__(self, dataframe, issues):

        self.df = dataframe
        self.issues = issues

    def generate(self):

        report = {}

        report["rows"] = len(self.df)
        report["columns"] = len(self.df.columns)
        report["issues"] = len(self.issues)

        report["issues_by_field"] = (
            self.issues["field"]
            .value_counts()
            .sort_values(ascending=False)
            .to_dict()
        )

        report["issues_by_rule"] = (
            self.issues["rule"]
            .value_counts()
            .sort_values(ascending=False)
            .to_dict()
        )

        report["quality_score"] = round(
            (1 - len(self.issues) / max(len(self.df), 1)) * 100,
            2
        )

        return report
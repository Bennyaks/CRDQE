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

        # -----------------------------------
        # Registration Status Statistics
        # -----------------------------------

        status_column = None

        if "Status" in self.df.columns:
            status_column = "Status"

        elif "status" in self.df.columns:
            status_column = "status"

        if status_column:

            report["current"] = (
                self.df[status_column]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("current")
                .sum()
            )

            report["late"] = (
                self.df[status_column]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("late")
                .sum()
            )

        else:

            report["current"] = 0
            report["late"] = 0

        # -----------------------------------
        # Issues by Field
        # -----------------------------------

        if not self.issues.empty:

            report["issues_by_field"] = (
                self.issues["field"]
                .value_counts()
                .sort_values(ascending=False)
                .to_dict()
            )

        else:

            report["issues_by_field"] = {}

        # -----------------------------------
        # Quality Score
        # -----------------------------------

        report["quality_score"] = round(
            (1 - len(self.issues) / max(len(self.df), 1)) * 100,
            2
        )
        mch_cases = 0

        # Only Death datasets have these columns
        if (
            "place_type" in self.df.columns
            and "death_certification" in self.df.columns
        ):

            home = (
                self.df["place_type"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            certification = (
                self.df["death_certification"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            mch_cases = (
                home.eq("home")
                &
                certification.str.contains(
                    "medical",
                    case=False,
                    na=False
                )
            ).sum()

        report["mch_cases"] = int(mch_cases)

        return report
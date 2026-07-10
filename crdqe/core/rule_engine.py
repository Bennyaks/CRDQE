"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Rule Engine

Purpose:
Execute all rules for a dataset.
===========================================================
"""

import pandas as pd


class RuleEngine:

    def __init__(self, rules, logger=None):
        self.rules = rules
        self.logger = logger

    def run(self, dataframe):

        df = dataframe.copy()

        all_issues = []

        for rule in self.rules:

            if self.logger:
                self.logger.info(f"Running {rule.__class__.__name__}")

            df, issues = rule.run(df)

            if self.logger:
                self.logger.info(
                    f"{rule.__class__.__name__}: {len(issues)} issue(s)"
                )

            if not issues.empty:
                all_issues.append(issues)

        if all_issues:
            issues_df = pd.concat(all_issues, ignore_index=True)
        else:
            issues_df = pd.DataFrame()

        return df, issues_df
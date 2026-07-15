"""
===========================================================
Collects issues from every validation rule.
===========================================================
"""

import pandas as pd


class IssueCollector:

    def __init__(self):
        self.issues = pd.DataFrame()

    def add(self, issues):

        if issues is None:
            return

        if isinstance(issues, list):
            if not issues:
                return
            issues = pd.DataFrame(issues)
        else:
            if issues.empty:
                return

        if self.issues.empty:
            self.issues = issues.copy()

        else:
            self.issues = pd.concat(
                [self.issues, issues],
                ignore_index=True
            )

    def to_dataframe(self):
        return self.issues

    def count(self):
        return len(self.issues)
import pandas as pd


class IssueStatistics:

    @staticmethod
    def generate(issues_df):

        if issues_df.empty:
            return pd.DataFrame()

        summary = (
            issues_df
            .groupby("issue")
            .size()
            .reset_index(name="count")
            .sort_values(
                "count",
                ascending=False
            )
        )

        return summary
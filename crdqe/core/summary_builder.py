import pandas as pd


class SummaryBuilder:

    @staticmethod
    def build(dataframe, issues):

        summary = {

            "Records Processed": len(dataframe),

            "Issues Found": len(issues),

            "Unique Fields Flagged":
                issues["field"].nunique(),

            "Rules Triggered":
                issues["rule"].nunique()

        }

        return pd.DataFrame(
            summary.items(),
            columns=["Metric", "Value"]
        )
    
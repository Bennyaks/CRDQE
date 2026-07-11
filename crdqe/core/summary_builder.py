"""
Builds the summary report for CRDQE.
"""

from datetime import datetime
import pandas as pd


class SummaryBuilder:

    @staticmethod
    def build(dataframe, issues):

        total_records = len(dataframe)
        total_issues = len(issues)

        quality_score = (
            ((total_records - total_issues) / total_records) * 100
            if total_records else 0
        )

        if quality_score >= 95:
            rating = "Excellent"
        elif quality_score >= 90:
            rating = "Very Good"
        elif quality_score >= 80:
            rating = "Good"
        elif quality_score >= 70:
            rating = "Fair"
        else:
            rating = "Needs Improvement"

        summary = [
            {
                "Metric": "Generated On",
                "Value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "Metric": "Records Processed",
                "Value": total_records
            },
            {
                "Metric": "Total Issues",
                "Value": total_issues
            },
            {
                "Metric": "Quality Score",
                "Value": f"{quality_score:.2f}%"
            },
            {
                "Metric": "Rating",
                "Value": rating
            }
        ]

        if not issues.empty:

            summary.extend([
                {
                    "Metric": "Errors",
                    "Value": (
                        issues["severity"]
                        .eq("Error")
                        .sum()
                    )
                },
                {
                    "Metric": "Warnings",
                    "Value": (
                        issues["severity"]
                        .eq("Warning")
                        .sum()
                    )
                }
            ])

        return pd.DataFrame(summary)
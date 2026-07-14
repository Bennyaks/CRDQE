"""
===========================================================
Status Processor

Purpose:
Calculate registration status from event date and
registration date.
===========================================================
"""

import pandas as pd


class StatusProcessor:

    @staticmethod
    def calculate(event_date, registration_date):

        if pd.isna(event_date) or pd.isna(registration_date):
            return ""

        days = (registration_date - event_date).days

        if days <= 60:
            return "Current"

        return "Late"

    @staticmethod
    def process(df, event_column):

        df["_calculated_status"] = df.apply(
            lambda row: StatusProcessor.calculate(
                row[event_column],
                row["registration_date"]
            ),
            axis=1
        )

        return df
"""
=========================================================
Status Calculator
---------------------------------------------------------
Determines whether a registration is Current or Late.

Rule:
Excel Formula

=IF(DATEDIF(EventDate, RegistrationDate,"M")>5,"LATE","CURRENT")
=========================================================
"""

import pandas as pd


class StatusCalculator:

    @staticmethod
    def calculate(event_date, registration_date):

        if pd.isna(event_date) or pd.isna(registration_date):
            return None

        event_date = pd.to_datetime(event_date, dayfirst=True, errors="coerce")
        registration_date = pd.to_datetime(
            registration_date,
            dayfirst=True,
            errors="coerce"
        )

        if pd.isna(event_date) or pd.isna(registration_date):
            return None

        months = (
            (registration_date.year - event_date.year) * 12
            + registration_date.month
            - event_date.month
        )

        # Replicates Excel DATEDIF(...,"M")
        if registration_date.day < event_date.day:
            months -= 1

        if months > 5:
            return "Late"

        return "Current"
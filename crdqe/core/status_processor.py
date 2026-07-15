"""
===========================================================
Status Processor

Purpose:
Calculate registration status from the event date
(Birth or Death) and the registration date.
===========================================================
"""

import pandas as pd


class StatusProcessor:

    # ===========================================================
    # Calculate Registration Status
    # ===========================================================

    @staticmethod
    def calculate_status(event_date, registration_date):

        if pd.isna(event_date) or pd.isna(registration_date):
            return None

        months = (
            (registration_date.year - event_date.year) * 12
            + (registration_date.month - event_date.month)
        )

        if months > 5:
            return "Late"

        return "Current"
    # ===========================================================
    # Swap Day and Month
    # ===========================================================

    @staticmethod
    def swap_day_month(date_value):

        if pd.isna(date_value):
            return None

        try:

            return pd.Timestamp(
                year=date_value.year,
                month=date_value.day,
                day=date_value.month
            )

        except ValueError:

            return None

    # ===========================================================
    # Validate Registration Status
    # ===========================================================

    @staticmethod
    def validate_status(df, event_column):

        issues = []
        corrections = []

        for index, row in df.iterrows():

            # -----------------------------------------
            # Read Dates
            # -----------------------------------------

            event_date = pd.to_datetime(
                row[event_column],
                dayfirst=True,
                errors="coerce"
            )

            registration_date = pd.to_datetime(
                row["registration_date"],
                dayfirst=True,
                errors="coerce"
            )

            if pd.isna(event_date) or pd.isna(registration_date):
                continue

            # -----------------------------------------
            # Calculate Status
            # -----------------------------------------

            calculated_status = StatusProcessor.calculate_status(
                event_date,
                registration_date
            )

            original_status = str(
                row["status"]
            ).strip().title()

            # -----------------------------------------
            # Status is Correct
            # -----------------------------------------

            if calculated_status == original_status:
                continue

            # -----------------------------------------
            # Health Facility Smart Correction
            # -----------------------------------------

            place = str(
                row["place_type"]
            ).strip().lower()

            if (
                place == "health facility"
                and original_status == "Current"
                and calculated_status == "Late"
            ):

                swapped_registration = StatusProcessor.swap_day_month(
                    registration_date
                )

                if swapped_registration is not None:

                    swapped_status = (
                        StatusProcessor.calculate_status(
                            event_date,
                            swapped_registration
                        )
                    )

                    if swapped_status == "Current":

                        df.at[
                            index,
                            "registration_date"
                        ] = swapped_registration.strftime("%d/%m/%Y")

                        df.at[
                            index,
                            "status"
                        ] = "Current"

                        corrections.append({

                            "Row": index + 2,

                            "Field": "registration_date",

                            "Old Value": registration_date.strftime("%d/%m/%Y"),

                            "New Value": swapped_registration.strftime("%d/%m/%Y"),

                            "Reason":
                                "Health Facility date automatically corrected"
                        })

                        continue

            # -----------------------------------------
            # Record Validation Issue
            # -----------------------------------------

            issues.append({

                "Row": index + 2,

                "Field": "status",

                "Issue":
                    f"Expected {calculated_status} but found {original_status}",

                "Value": original_status
            })

        return df, issues, corrections
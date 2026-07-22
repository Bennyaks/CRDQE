"""
===========================================================
Status Processor

Purpose:
Calculate registration status from the event date
(Birth or Death) and the registration date.

Also:
- Flags any record whose registration date falls outside
  the user-selected registration month (independent check,
  not tied to the status/swap logic below).
- Applies a "smart correction" for Health Facility records
  that come back Late: tries swapping the day/month of the
  registration date first, then (if that doesn't resolve it)
  the event date (DOB/DOD) instead. If neither swap brings
  the status back to Current, the record is left untouched
  and flagged for the user to review.
- Home records that mismatch are always just flagged for
  review -- never auto-corrected, since a late Home
  registration is plausible.
===========================================================
"""

import pandas as pd


MONTH_NAME_TO_NUMBER = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


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
    def validate_status(
        df,
        event_column,
        registration_month=None,
        registration_year=None
    ):

        issues = []
        corrections = []

        target_month_number = None

        if registration_month:

            target_month_number = MONTH_NAME_TO_NUMBER.get(
                str(registration_month).strip().lower()
            )

        target_year_number = None

        if registration_year:

            try:
                target_year_number = int(str(registration_year).strip())
            except (TypeError, ValueError):
                target_year_number = None

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
            # Registration Month Consistency Check
            # (independent of the status logic below --
            # runs regardless of whether status matches)
            # -----------------------------------------

            if (
                target_month_number is not None
                and registration_date.month != target_month_number
            ):

                issues.append({

                    "entry_number": row.get("entry_number", None),

                    "field": "registration_date",

                    "value": registration_date.strftime("%d/%m/%Y"),

                    "issue": (
                        f"Registration date month "
                        f"({registration_date.strftime('%B')}) does not "
                        f"match the selected registration month "
                        f"({registration_month})"
                    ),

                    "severity": "Warning"
                })

            # -----------------------------------------
            # Registration Year Consistency Check
            # (independent of the status logic below --
            # runs regardless of whether status matches)
            # -----------------------------------------

            if (
                target_year_number is not None
                and registration_date.year != target_year_number
            ):

                issues.append({

                    "entry_number": row.get("entry_number", None),

                    "field": "registration_date",

                    "value": registration_date.strftime("%d/%m/%Y"),

                    "issue": (
                        f"Registration date year "
                        f"({registration_date.year}) does not "
                        f"match the selected registration year "
                        f"({registration_year})"
                    ),

                    "severity": "Warning"
                })

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

            place = str(
                row["place_type"]
            ).strip().lower()

            # -----------------------------------------
            # Health Facility Smart Correction
            #
            # IMPORTANT: this runs whenever a Health Facility
            # record calculates as Late -- regardless of what
            # the document's own status column says. A Health
            # Facility record can never plausibly be Late, so
            # even a record where the document already (wrongly)
            # agrees with a Late calculation still needs this
            # check; it isn't limited to disagreements between
            # the document and the calculation.
            # -----------------------------------------

            if (
                place == "health facility"
                and calculated_status == "Late"
            ):

                # ---- Attempt 1: swap the registration date ----

                swapped_registration = StatusProcessor.swap_day_month(
                    registration_date
                )

                if swapped_registration is not None:

                    status_after_reg_swap = (
                        StatusProcessor.calculate_status(
                            event_date,
                            swapped_registration
                        )
                    )

                    if status_after_reg_swap == "Current":

                        df.at[index, "registration_date"] = (
                            swapped_registration.strftime("%d/%m/%Y")
                        )

                        df.at[index, "status"] = "Current"

                        corrections.append({

                            "Row": index + 2,

                            "Field": "registration_date",

                            "Old Value":
                                registration_date.strftime("%d/%m/%Y"),

                            "New Value":
                                swapped_registration.strftime("%d/%m/%Y"),

                            "Reason": (
                                "Health Facility date automatically "
                                "corrected (registration date day/month "
                                "swapped)"
                            )
                        })

                        continue

                # ---- Attempt 2: swap the event date (DOB/DOD) ----

                swapped_event = StatusProcessor.swap_day_month(
                    event_date
                )

                if swapped_event is not None:

                    status_after_event_swap = (
                        StatusProcessor.calculate_status(
                            swapped_event,
                            registration_date
                        )
                    )

                    if status_after_event_swap == "Current":

                        df.at[index, event_column] = (
                            swapped_event.strftime("%d/%m/%Y")
                        )

                        df.at[index, "status"] = "Current"

                        corrections.append({

                            "Row": index + 2,

                            "Field": event_column,

                            "Old Value":
                                event_date.strftime("%d/%m/%Y"),

                            "New Value":
                                swapped_event.strftime("%d/%m/%Y"),

                            "Reason": (
                                "Health Facility date automatically "
                                "corrected (event date day/month swapped)"
                            )
                        })

                        continue

                # Neither swap resolved it -- fall through and flag below,
                # with a message explaining why no auto-correction was
                # possible (so it doesn't look like an inconsistent
                # failure -- day/month swapping is only mathematically
                # possible when the day is <= 12).

                issues.append({

                    "entry_number": row.get("entry_number", None),

                    "field": "status",

                    "value": original_status,

                    "issue": (
                        "Health Facility record still shows Late after "
                        "attempting date corrections. Registration date "
                        f"and/or {event_column} could not be swapped "
                        "(day component > 12, so no alternate d/m/y "
                        "interpretation exists). Please review manually."
                    ),

                    "severity": "Error"
                })

                continue

            # -----------------------------------------
            # Record Validation Issue
            # (Home records, and any other unresolved mismatch --
            # Health Facility Late is handled entirely above)
            # -----------------------------------------

            if calculated_status == original_status:
                continue

            issues.append({

                "entry_number": row.get("entry_number", None),

                "field": "status",

                "value": original_status,

                "issue":
                    f"Expected {calculated_status} but found {original_status}",

                "severity": "Error"
            })

        return df, issues, corrections
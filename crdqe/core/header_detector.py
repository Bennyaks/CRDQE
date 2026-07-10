"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Header Detector

Purpose:
Locate the actual header row in a worksheet.
===========================================================
"""

import pandas as pd


class HeaderDetector:

    HEADER_KEYWORDS = [
        "date of birth",
        "sex",
        "entry number",
        "mother",
        "place of birth",
        "date of registration",
        "status",
        "date of death",
        "cause of death",
    ]

    @staticmethod
    def find_header_row(workbook_path, worksheet, max_rows=20):
        """
        Search the first few rows for the actual header.
        """

        preview = pd.read_excel(
            workbook_path,
            sheet_name=worksheet,
            header=None,
            nrows=max_rows,
            engine="openpyxl"
        )

        best_row = None
        best_score = -1

        for index, row in preview.iterrows():

            text = " ".join(
                str(value).lower()
                for value in row
                if pd.notna(value)
            )

            score = sum(
                keyword in text
                for keyword in HeaderDetector.HEADER_KEYWORDS
            )

            if score > best_score:
                best_score = score
                best_row = index

        return best_row
"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Column Standardizer

Purpose:
Standardize Excel column names.
===========================================================
"""

import re


class ColumnStandardizer:

    @staticmethod
    def clean(columns):
        """
        Standardize column names.
        """

        cleaned = []

        for column in columns:

            column = str(column)

            # Remove line breaks
            column = column.replace("\n", " ")
            column = column.lower()

            column = column.replace(".", "")

            column = column.replace("_", " ")

            column = re.sub(r"\s+", " ", column)

            column = column.strip()

            # Collapse multiple spaces
            column = re.sub(r"\s+", " ", column)

            # Remove leading/trailing spaces
            column = column.strip()

            # Normalize parentheses spacing
            column = column.replace(" (", "(").replace("( ", "(")
            column = column.replace(" )", ")")

            cleaned.append(column)

        return cleaned
    
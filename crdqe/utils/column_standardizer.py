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
    def standardize(column):
        """
        Standardize a single column name. This is the single
        source of truth for the normalization rules -- clean()
        (bulk) and standardize() (single string) must always
        agree, or header text normalized one at a time (e.g. in
        SchemaMapper, against schema aliases) will drift out of
        sync with header text normalized in bulk (the actual
        workbook columns in engine.py), causing header-vs-alias
        matches to silently score lower than they should.
        """

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

        return column

    @staticmethod
    def clean(columns):
        """
        Standardize a list of column names.
        """

        return [
            ColumnStandardizer.standardize(column)
            for column in columns
        ]
    
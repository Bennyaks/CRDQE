"""
===========================================================
Schema Mapper

Maps workbook columns to the CRDQE schema using:

1. Alias Matching
2. Fuzzy Matching
3. Value Matching (fallback)

Supports both:

• source_columns
• derived_columns

===========================================================
"""

from difflib import SequenceMatcher

from crdqe.utils.column_standardizer import ColumnStandardizer
from crdqe.core.value_matcher import ValueMatcher


def normalize(text):
    """
    Normalize text for similarity comparison.
    """
    if text is None:
        return ""

    try:
        return ColumnStandardizer().standardize(text)
    except Exception:
        return str(text).strip().lower()


class SchemaMapper:

    def __init__(self, schema):

        self.schema = {}

        # ------------------------------------------
        # Source Columns
        # ------------------------------------------

        self.schema.update(
            schema.get(
                "source_columns",
                {}
            )
        )

        # ------------------------------------------
        # Derived Columns
        # ------------------------------------------

        self.schema.update(
            schema.get(
                "derived_columns",
                {}
            )
        )

        print("\n========== LOADED SCHEMA ==========")

        # for field in self.schema:
            # print(field)

        # print("===================================")
        self.value_matcher = ValueMatcher(self.schema)
    # ===========================================================
    # Column Similarity
    # ===========================================================

    def similarity(self, text1, text2):
        """
        Returns similarity score between two strings.
        """

        return SequenceMatcher(
            None,
            normalize(text1),
            normalize(text2)
        ).ratio()
    # ===========================================================
    # Map Columns
    # ===========================================================

    def map_columns(self, dataframe):

        mapping = {}
        used_columns = set()

        print("\n========== COLUMN MAPPING ==========\n")

        for column in dataframe.columns:

            best_field = None
            best_score = 0

            for field, details in self.schema.items():
            

                aliases = details.get("aliases", [])

                for alias in aliases:

                    score = self.similarity(column, alias)

                    if score > best_score:

                        best_score = score
                        best_field = field

            if best_score >= 0.90:

                mapping[column] = best_field
                used_columns.add(column)

                print(
                    f"{column} ---> {best_field} ({best_score:.0%})"
                )

            else:

                print(
                    f"{column} ---> NOT MAPPED BY HEADER ({best_score:.0%})"
                )

        # ------------------------------------------
        # Value Matching (fallback via ValueMatcher --
        # identifies columns by their actual values:
        # enum/valid_values, numeric range, or date format)
        # ------------------------------------------

        value_mapping = self.value_match(dataframe, used_columns)

        mapping.update(value_mapping)

        print("\n====================================\n")

        # Rename and keep mapped columns
        mapped_columns = list(mapping.keys())

        dataframe = dataframe[mapped_columns]

        dataframe = dataframe.rename(columns=mapping)

        return dataframe

    # ==========================================================
    # Value Matching (fallback)
    # ==========================================================

    def value_match(self, dataframe, used_columns):
        """
        For columns that didn't map to any field via header/alias
        similarity, delegate to ValueMatcher to identify the field
        from its actual values (enum membership, numeric range, or
        date format).
        """

        mapping = {}

        for column in dataframe.columns:

            if column in used_columns:
                continue

            field, confidence = self.value_matcher.match(
                dataframe[column]
            )

            if field:

                mapping[column] = field
                used_columns.add(column)

                print(
                    f"{column} ---> {field} "
                    f"(Value Match {confidence}%)"
                )

        return mapping
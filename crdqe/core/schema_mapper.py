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
        self.value_matcher = ValueMatcher(schema)
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

                print(
                    f"{column} ---> {best_field} ({best_score:.0%})"
                )

            else:

                print(
                    f"{column} ---> NOT MAPPED ({best_score:.0%})"
                )

        print("\n====================================\n")
        

        # Rename and keep mapped columns
        mapped_columns = list(mapping.keys())

        dataframe = dataframe[mapped_columns]

        dataframe = dataframe.rename(columns=mapping)

        return dataframe
    # ==========================================================
# Value Matching
# ==========================================================

def value_match(self, dataframe, used_columns):

    mapping = {}

    for column in dataframe.columns:

        if column in used_columns:
            continue

        values = (
            dataframe[column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
        )

        values = set(values)

        best_field = None
        best_score = 0

        for field, details in self.fields.items():

            valid = details.get("Valid_values", {})

            if not valid:
                continue

            expected = {
                str(v).strip().lower()
                for v in valid.values()
            }

            if len(expected) == 0:
                continue

            score = len(values & expected) / len(expected)

            if score > best_score:
                best_score = score
                best_field = field

        if best_field and best_score >= 0.50:

            mapping[column] = best_field
            used_columns.add(column)

            print(
                f"{column} ---> {best_field} "
                f"(Value Match {best_score:.0%})"
            )
    # ------------------------------------------
    # Value Matching
    # ------------------------------------------

    value_mapping = self.value_match(
        dataframe,
        used_columns
    )

    mapping.update(value_mapping)

    return mapping


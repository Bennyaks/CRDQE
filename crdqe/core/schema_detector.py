"""
=========================================================
Schema Detector
---------------------------------------------------------
Detects the correct schema fields for a dataset using
multiple strategies.

Current Strategies:
    1. Alias Matching
    2. Value Matching

Future Strategies:
    3. Fuzzy Matching
    4. Type Profiling
    5. Confidence Scoring
=========================================================
"""

from difflib import SequenceMatcher
from crdqe.utils.column_standardizer import ColumnStandardizer
from crdqe.utils.text_normalizer import normalize


class SchemaDetector:

    def __init__(self, schema):

        self.schema = schema

    # =====================================================
    # Main Detection
    # =====================================================

    def detect(self, dataframe):

        columns = list(dataframe.columns)

        mapping = {}
        confidence = {}

        standardized_columns = {
            normalize(
                ColumnStandardizer.clean([column])[0]
            ): column
            for column in columns
        }
        
        print(standardized_columns)
        print("\nSTANDARDIZED COLUMNS")

        for key, value in standardized_columns.items():
            print(value, "---->", key)
        print("\nALIASES")

        for field, properties in self.schema.items():

            print(field)

            for alias in properties.get("aliases", []):

                print(
                    alias,
                    "->",
                    ColumnStandardizer.clean([alias])[0]
                )

        used_columns = set()

        for field, properties in self.schema.items():

            aliases = properties.get("aliases", [])

            # -----------------------------------------
            # Strategy 1 : Alias Matching
            # -----------------------------------------

            matched = self.alias_match(
                aliases,
                standardized_columns,
                used_columns
            )

            score = 100


            # -----------------------------------------
            # Strategy 2 : Value Matching
            # -----------------------------------------

            if matched is None:

                matched, score = self.value_match(
                    properties,
                    dataframe,
                    used_columns
                )

            # -----------------------------------------

            if matched:

                mapping[matched] = field
                confidence[field] = score
                used_columns.add(matched)
        
        return mapping, confidence
        

    # =====================================================
    # Alias Matching
    # =====================================================

    def alias_match(
        self,
        aliases,
        standardized_columns,
        used_columns
    ):

        aliases = [
            normalize(
                ColumnStandardizer.clean([alias])[0]
            )
            for alias in aliases
        ]

        for alias in aliases:

            best_column = None
            best_score = 0

            for std_col, original in standardized_columns.items():

                score = SequenceMatcher(
                    None,
                    alias,
                    std_col
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_column = original

            if best_score >= 0.90 and best_column not in used_columns:
                return best_column
    
    

    # =====================================================
    # Value Matching
    # =====================================================

    def value_match(
        self,
        properties,
        dataframe,
        used_columns
    ):

        expected = properties.get("expected_values")

        if not expected:

            return None, 0

        expected = {
            normalize(str(value))
            for value in expected
        }

        best_column = None
        best_score = 0

        for column in dataframe.columns:

            if column in used_columns:
                continue

            values = (
                dataframe[column]
                .dropna()
                .astype(str)
                .head(50)
            )

            if len(values) == 0:
                continue

            matches = 0

            for value in values:

                if normalize(value) in expected:
                    matches += 1

            score = matches / len(values)

            if score > best_score:

                best_score = score
                best_column = column

        if best_score >= 0.80:

            return best_column, int(best_score * 100)

        return None, 0
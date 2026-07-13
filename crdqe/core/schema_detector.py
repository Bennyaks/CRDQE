"""
=========================================================
Schema Detector
---------------------------------------------------------
Detects the correct schema fields for a dataset using
multiple strategies.

Current Strategy:
    1. Alias Matching

Future Strategies:
    2. Fuzzy Matching
    3. Value Profiling
    4. Confidence Scoring
=========================================================
"""

from crdqe.utils.column_standardizer import ColumnStandardizer


class SchemaDetector:

    def __init__(self, schema):

        self.schema = schema

    def detect(self, columns):

        columns = list(columns)

        mapping = {}
        confidence = {}

        standardized_columns = {
            ColumnStandardizer.clean([column])[0]: column
            for column in columns
        }

        for field, properties in self.schema.items():

            aliases = properties.get("aliases", [])

            aliases = [
                ColumnStandardizer.clean([alias])[0]
                for alias in aliases
            ]

            matched = None

            for alias in aliases:

                if alias in standardized_columns:

                    matched = standardized_columns[alias]
                    break

            if matched:

                mapping[matched] = field
                confidence[field] = 100
        print(self.schema)

        return mapping, confidence
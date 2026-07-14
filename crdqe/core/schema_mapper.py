"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Schema Mapper

Purpose:
Maps workbook columns to the internal CRDQE schema using
alias matching and fuzzy matching.
===========================================================
"""

import yaml
from difflib import SequenceMatcher

from crdqe.utils.text_normalizer import normalize


class SchemaMapper:

    def __init__(self, schema_file):

        with open(schema_file, "r", encoding="utf-8") as file:
            self.schema = yaml.safe_load(file)

    def get_schema(self):
        return self.schema

    def similarity(self, text1, text2):
        """
        Returns similarity between two strings.
        """

        return SequenceMatcher(
            None,
            text1,
            text2
        ).ratio()

    def map_columns(self, dataframe):

        mapping = {}

        print("\n========== COLUMN MAPPING ==========\n")

        for column in dataframe.columns:

            best_field = None
            best_score = 0

            for field, details in self.schema["source_columns"].items():

                aliases = [
                    normalize(alias)
                    for alias in details.get("aliases", [])
                ]

                for alias in aliases:

                    score = self.similarity(
                        normalize(column),
                        alias
                    )

                    if score > best_score:
                        best_score = score
                        best_field = field

            if best_score >= 0.90:

                mapping[column] = best_field

                print(
                    f"{column}  --->  {best_field} ({best_score:.0%})"
                )

            else:

                print(
                    f"{column}  --->  NOT MAPPED ({best_score:.0%})"
                )

        print("\n====================================\n")

        return dataframe.rename(columns=mapping)
"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Schema Mapper

Purpose:
Map workbook columns to internal schema.
===========================================================
"""

from pathlib import Path
import yaml

from crdqe.utils.text_normalizer import normalize


class SchemaMapper:

    def __init__(self, schema_file):

        with open(schema_file, "r", encoding="utf-8") as file:
            self.schema = yaml.safe_load(file)

    def get_schema(self):
        return self.schema

    def map_columns(self, dataframe):

        mapping = {}

        for field, details in self.schema["source_columns"].items():

            print(f"{field} --> {type(details)}")

            if not isinstance(details, dict):
                raise TypeError(
                    f"Schema error: '{field}' should be a dictionary but is {type(details)}.\nValue: {details}"
                )

            aliases = details.get("aliases", [])
            aliases = [normalize(alias) for alias in aliases]

            for column in dataframe.columns:

                if normalize(column) in aliases:
                    mapping[column] = field

        return dataframe.rename(columns=mapping)
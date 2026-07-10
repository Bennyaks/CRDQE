"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Schema Validator

Purpose:
Validate that all required columns exist.
===========================================================
"""


class SchemaValidator:

    @staticmethod
    def validate(dataframe, schema):

        required = list(schema["source_columns"].keys())

        missing = [
            column
            for column in required
            if column not in dataframe.columns
        ]

        extra = [
            column
            for column in dataframe.columns
            if column not in required
        ]

        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "extra": extra,
        }
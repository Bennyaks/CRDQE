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

        # Source columns (expected straight from the workbook) and
        # derived columns (e.g. "status") are both real, expected
        # fields -- a field being "derived" describes where it's
        # computed/cross-checked from, not whether it needs to be
        # present. Whether a field is actually required is driven
        # by each field's own "required" flag in the schema, not
        # by which section it lives in or a hardcoded field name.

        fields = {}
        fields.update(schema.get("source_columns", {}) or {})
        fields.update(schema.get("derived_columns", {}) or {})

        required = [
            field
            for field, details in fields.items()
            if details.get("required")
        ]

        missing = [
            column
            for column in required
            if column not in dataframe.columns
        ]

        extra = [
            column
            for column in dataframe.columns
            if column not in fields
        ]

        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "extra": extra,
        }
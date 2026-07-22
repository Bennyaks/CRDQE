import pandas as pd
import re


class PlaceholderProcessor:
    """
    Replace placeholder values with standardized values.
    """

    # Common placeholders used by data entry clerks
    PLACEHOLDERS = {
        "",
        "-",
        "--",
        "---",
        ".",
        "..",
        "...",
        "/",
        "//",
        "\\",
        "n/a",
        "na",
        "null",
        "none",
        "nil",
        "missing",
    }

    @classmethod
    def process(cls, df, schema):
        df = df.copy()

        replacements = 0

        # Cover both source_columns and derived_columns (e.g. "status")
        # -- a raw placeholder can show up in either.
        fields = {}
        fields.update(schema.get("source_columns", {}) or {})
        fields.update(schema.get("derived_columns", {}) or {})

        for field, properties in fields.items():

            if field not in df.columns:
                continue

            # The schema declares each field's type under "datatype",
            # not "type" -- using the wrong key here meant every field
            # silently fell back to "string", so numeric/date fields
            # were getting the text "Not Stated" instead of a real
            # missing value (pd.NA).
            dtype = properties.get("datatype", "string")

            for index, value in df[field].items():

                if pd.isna(value):
                    continue

                value_str = str(value).strip()

                # lowercase comparison
                if value_str.lower() in cls.PLACEHOLDERS:

                    if dtype == "string":
                        df.at[index, field] = "Not Stated"
                    else:
                        df.at[index, field] = pd.NA

                    replacements += 1
                    continue

                # value contains ONLY symbols
                if re.fullmatch(r"[\W_]+", value_str):

                    if dtype == "string":
                        df.at[index, field] = "Not Stated"
                    else:
                        df.at[index, field] = pd.NA

                    replacements += 1
                    continue

        print(f"Placeholder replacements: {replacements}")

        return df
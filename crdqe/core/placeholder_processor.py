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

        for field, properties in schema["source_columns"].items():

            if field not in df.columns:
                continue

            dtype = properties.get("type", "string")

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

        print(f"Placeholder replacements: {replacements}")

        return df
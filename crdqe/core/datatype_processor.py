import pandas as pd


class DataTypeProcessor:
    """
    Converts dataframe columns to their expected datatypes
    before validation begins.
    """

    @staticmethod
    def process(df, schema):

        df = df.copy()

        for field, details in schema["source_columns"].items():

            if field not in df.columns:
                continue

            datatype = details.get("datatype")

            if datatype == "string":

                df[field] = (
                    df[field]
                    .astype("string")
                    .str.strip()
                )

            elif datatype == "integer":

                numeric = pd.to_numeric(
                    df[field],
                    errors="coerce"
                )

                non_null = numeric.dropna()

                # Only force a clean Int64 cast when every present value
                # genuinely is a whole number. A field with a fractional
                # value (e.g. a data-entry typo like age "30.5") would
                # otherwise raise "cannot safely cast non-equivalent
                # float64 to int64" and crash the entire pipeline over
                # what should just be a flaggable validation issue.

                all_whole_numbers = (
                    non_null.empty
                    or (non_null % 1 == 0).all()
                )

                if all_whole_numbers:
                    df[field] = numeric.astype("Int64")
                else:
                    df[field] = numeric

            elif datatype == "float":

                df[field] = pd.to_numeric(
                    df[field],
                    errors="coerce"
                )

            elif datatype == "date":

                df[field] = pd.to_datetime(
                    df[field],
                    errors="coerce",
                    dayfirst=True
                )

        return df
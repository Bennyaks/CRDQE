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

                df[field] = pd.to_numeric(
                    df[field],
                    errors="coerce"
                ).astype("Int64")

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
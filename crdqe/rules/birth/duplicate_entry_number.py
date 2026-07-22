"""
===========================================================
Birth Rule

Duplicate Entry Number
===========================================================
"""

from crdqe.core.base_rule import BaseRule


class DuplicateEntryNumberRule(BaseRule):

    FIELD = "entry_number"

    def __init__(self, schema=None):
        super().__init__(schema)

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        values = (
            df[self.FIELD]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        duplicates = (
            values.ne("")
            & values.duplicated(keep=False)
        )

        for index, row in df.iterrows():

            value = values.iloc[index]

            # Ignore missing values
            if self.is_missing(value):
                continue

            # Duplicate Entry Number
            if duplicates.iloc[index]:

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message="Duplicate Entry Number"
                )

        return df, self.get_issues()
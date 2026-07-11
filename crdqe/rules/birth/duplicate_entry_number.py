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

        mask = (
            values.ne("") &
            values.duplicated(keep=False)
        )

        for index in df.index[mask]:

            self.add_issue(
                row=index,
                field=self.FIELD,
                issue="Duplicate Entry Number",
                value=df.at[index, self.FIELD]
            )

        return df, self.get_issues()
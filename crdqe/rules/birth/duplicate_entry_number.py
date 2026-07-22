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

        for index, row in df.iterrows():

            value = row[self.FIELD]

            if self.is_missing(value):

                self.add_issue(
                    row=index,
                    field=self.FIELD,
                    value=value,
                    issue=f"Missing {self.TITLE}"
                )

                continue
        return df, self.get_issues()
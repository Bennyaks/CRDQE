"""
===========================================================
Generic Text Rule
===========================================================
"""

from crdqe.core.base_rule import BaseRule


class TextRule(BaseRule):

    FIELD = None

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        for index, row in df.iterrows():

            value = row[self.FIELD]

            if self.is_missing(value):

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field=self.FIELD,
                    value=value,
                    message=f"Missing {self.TITLE}"
                )
                continue

            # Clean the text
            value = str(value).strip()
            value = " ".join(value.split())
            

            df.at[index, self.FIELD] = value

        return df, self.get_issues()
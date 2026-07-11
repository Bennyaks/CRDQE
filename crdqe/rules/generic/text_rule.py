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

        for index, value in df[self.FIELD].items():

            if self.is_missing(value):

                self.add_issue(
                    row=index,
                    field=self.FIELD,
                    issue=f"Missing {self.TITLE}"
                )
                continue

            # Clean the text
            value = str(value).strip()
            value = " ".join(value.split())
            value = value.title()

            df.at[index, self.FIELD] = value

        return df, self.get_issues()
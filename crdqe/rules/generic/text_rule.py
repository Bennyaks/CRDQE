"""
===========================================================
Generic Text Rule
===========================================================
"""

from crdqe.core.base_rule import BaseRule


class TextRule(BaseRule):

    FIELD = None

    def validate(self, value):
        """
        Override in child classes if needed.
        """
        return True

    def run(self, dataframe):

        df = self.start(dataframe)

        for index, value in df[self.FIELD].items():

            if self.is_missing(value):

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Missing {self.FIELD}"
                )
                continue

            cleaned = str(value).strip()

            if cleaned == "":

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Blank {self.FIELD}"
                )
                continue

            if not self.validate(cleaned):

                self.add_issue(
                    index,
                    self.FIELD,
                    f"Invalid {self.FIELD}",
                    cleaned
                )
                continue

            df.at[index, self.FIELD] = cleaned

        return df, self.get_issues()
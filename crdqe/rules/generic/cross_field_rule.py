"""
===========================================================
Generic Cross Field Rule
===========================================================
"""

from crdqe.core.base_rule import BaseRule


class CrossFieldRule(BaseRule):

    def validate(self, index, row):
        """
        Override in child rules.
        """
        raise NotImplementedError

    def run(self, dataframe):

        df = self.start(dataframe)

        for index, row in df.iterrows():
            self.validate(index, row)

        return df, self.get_issues()
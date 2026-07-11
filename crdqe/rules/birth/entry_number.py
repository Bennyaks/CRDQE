from crdqe.core.base_rule import BaseRule


class EntryNumberRule(BaseRule):

    FIELD = "entry_number"

    def __init__(self, schema=None):
        super().__init__(schema)

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        for index, value in df[self.FIELD].items():

            if self.is_missing(value):

                self.add_issue(
                    row=index,
                    field=self.FIELD,
                    issue="Missing Entry Number"
                )

                continue

            cleaned = str(value).strip()

            df.at[index, self.FIELD] = cleaned

        return df, self.get_issues()
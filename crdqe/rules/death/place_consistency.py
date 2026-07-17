from crdqe.core.base_rule import BaseRule


class PlaceConsistencyRule(BaseRule):

    def __init__(self, schema=None):
        super().__init__(schema)

    def run(self, dataframe):

        self.issues = []

        df = dataframe.copy()

        for index, row in df.iterrows():

            place = str(row["place_of_death"]).strip()
            place_type = str(row["place_type"]).strip().lower()

            if place == "":

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field="place_of_death",
                    value=row["place_of_death"],
                    message="Missing Place of Death"
                )

                continue

            if place_type not in [
                "home",
                "health facility"
            ]:

                self.add_issues(
                    issues=self.issues,
                    row=row,
                    field="place_type",
                    value=row["place_type"],
                    message="Invalid Place Type"
                )

        return df, self.get_issues()
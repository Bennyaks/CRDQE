"""
===========================================================
Schema Mapper

Maps workbook columns to the CRDQE schema using both header
(alias/fuzzy) matching and value matching for EVERY column,
then resolves conflicts when two columns end up competing for
the same destination field.

Design
------
- Header match: fuzzy similarity between the column name and
  each field's known aliases.
- Value match: ValueMatcher identifies a field from the
  column's actual data (enum membership, numeric range, or
  date format).
- A column's final field is whichever signal is stronger. This
  lets a mislabeled header -- e.g. a column literally titled
  "Type of Registration" that actually contains "Lay
  Reporting"/"Medically Certified" values -- still get
  correctly identified and renamed to "death_certification"
  based on what the data actually is, instead of being trusted
  at face value or silently left unmapped.
- If two columns both resolve to the same destination field,
  the one with stronger, more corroborated evidence wins.
  "Double confirmed" (header AND value independently agree on
  the same field) always outranks a single-signal match, even
  when the single-signal's raw score is numerically equal or
  higher. Among matches with the same corroboration level, the
  higher confidence score wins.
===========================================================
"""

from difflib import SequenceMatcher

from crdqe.utils.column_standardizer import ColumnStandardizer
from crdqe.core.value_matcher import ValueMatcher


# Header similarity at/above this is trusted on its own,
# without needing value confirmation.
HEADER_TRUST_THRESHOLD = 0.90


def normalize(text):
    """
    Normalize text for similarity comparison.
    """
    if text is None:
        return ""

    try:
        return ColumnStandardizer().standardize(text)
    except Exception:
        return str(text).strip().lower()


class SchemaMapper:

    def __init__(self, schema):


        self.schema = {}

        # ------------------------------------------
        # Source Columns
        # ------------------------------------------

        self.schema.update(
            schema.get(
                "source_columns",
                {}
            )
        )

        # ------------------------------------------
        # Derived Columns
        # ------------------------------------------

        self.schema.update(
            schema.get(
                "derived_columns",
                {}
            )
        )

        self.value_matcher = ValueMatcher(self.schema)

    # ===========================================================
    # Column Similarity
    # ===========================================================

    def similarity(self, text1, text2):
        """
        Returns similarity score between two strings.
        """

        return SequenceMatcher(
            None,
            normalize(text1),
            normalize(text2)
        ).ratio()

    # ===========================================================
    # Header Matching
    # ===========================================================
    def header_match(self, column):
        """
        Returns the best matching schema field for a column header.

        Returns:
            (best_field, best_score)

        where:
            best_field -> schema field name
            best_score -> similarity score (0.0 - 1.0)
        """

        best_field = None
        best_score = 0.0

        column_norm = normalize(column)

        for field, details in self.schema.items():

            for alias in details.get("aliases", []):

                alias_norm = normalize(alias)

                # -----------------------------------------
                # Exact / containment match
                # -----------------------------------------

                if (
                    column_norm == alias_norm
                    or column_norm.startswith(alias_norm)
                    or alias_norm.startswith(column_norm)
                    or column_norm in alias_norm
                    or alias_norm in column_norm
                ):

                    score = 1.0

                # -----------------------------------------
                # Fuzzy match
                # -----------------------------------------

                else:

                    score = self.similarity(
                        column_norm,
                        alias_norm
                    )

                # -----------------------------------------
                # Keep best match
                # -----------------------------------------

                if score > best_score:

                    best_score = score
                    best_field = field

        return best_field, best_score

    # ===========================================================
    # Per-Column Decision (header vs value)
    # ===========================================================

    def _decide_column(self, column, series):
        """
        Decide the most likely destination field for a column by combining
        header similarity and value analysis.

        Priority:
            1. Header + Value agree.
            2. Strong Header match.
            3. Strong Value match.
            4. Otherwise, reject the mapping.
        """

        # ----------------------------------------------------------
        # Gather evidence
        # ----------------------------------------------------------

        header_field, header_score = self.header_match(column)
        header_score *= 100

        value_field, value_score = self.value_matcher.match(series)

        # ----------------------------------------------------------
        # Header and values agree
        # ----------------------------------------------------------

        if (
            header_field
            and value_field
            and header_field == value_field
        ):

            return {
                "column": column,
                "field": header_field,
                "confidence": max(header_score, value_score),
                "double_confirmed": True,
                "reason": "Header + Value Match",
                "header_field": header_field,
                "header_score": header_score,
                "value_field": value_field,
                "value_score": value_score,
            }

        # ----------------------------------------------------------
        # Strong Header Match
        # Useful for date columns where value matching cannot
        # distinguish between different date fields.
        # ----------------------------------------------------------

        if (
            header_field
            and header_score >= HEADER_TRUST_THRESHOLD * 100
        ):

            return {
                "column": column,
                "field": header_field,
                "confidence": header_score,
                "double_confirmed": False,
                "reason": "Header Match",
                "header_field": header_field,
                "header_score": header_score,
                "value_field": value_field,
                "value_score": value_score,
            }

        # ----------------------------------------------------------
        # Strong Value Match
        # Used when the header is incorrect but the column values
        # clearly identify the correct field.
        # ----------------------------------------------------------

        if value_field:

            return {
                "column": column,
                "field": value_field,
                "confidence": value_score,
                "double_confirmed": False,
                "reason": "Value Match",
                "header_field": header_field,
                "header_score": header_score,
                "value_field": value_field,
                "value_score": value_score,
            }

        # ----------------------------------------------------------
        # No reliable mapping
        # ----------------------------------------------------------

        return None
    # ===========================================================
    # Map Columns
    # ===========================================================

    def map_columns(self, dataframe):

        print("\n========== COLUMN MAPPING ==========\n")

        # ------------------------------------------
        # Step 1: decide a candidate field for every
        # column independently, using both signals.
        # ------------------------------------------

        candidates = []

        for column in dataframe.columns:

            decision = self._decide_column(column, dataframe[column])

            if decision is None:

                print(f"{column} ---> NOT MAPPED")
                continue

            candidates.append(decision)

        # ------------------------------------------
        # Step 2: resolve conflicts -- if multiple
        # columns want the same field, keep whichever
        # has the strongest, most corroborated evidence.
        # ------------------------------------------

        winners = {}  # field -> decision dict

        for decision in candidates:

            field = decision["field"]
            existing = winners.get(field)

            if existing is None:

                winners[field] = decision
                continue

            new_rank = (
                decision["double_confirmed"],
                decision["confidence"]
            )

            existing_rank = (
                existing["double_confirmed"],
                existing["confidence"]
            )

            if new_rank > existing_rank:

                print(
                    f"{decision['column']} ---> '{field}' replaces "
                    f"{existing['column']} "
                    f"(stronger: {decision['reason']} "
                    f"{decision['confidence']:.0f}%"
                    f"{' [double-confirmed]' if decision['double_confirmed'] else ''} "
                    f"beats {existing['reason']} "
                    f"{existing['confidence']:.0f}%"
                    f"{' [double-confirmed]' if existing['double_confirmed'] else ''})"
                )

                winners[field] = decision

            else:

                print(
                    f"{decision['column']} ---> CONFLICT for '{field}', "
                    f"kept {existing['column']} "
                    f"({existing['reason']} {existing['confidence']:.0f}%"
                    f"{' [double-confirmed]' if existing['double_confirmed'] else ''} "
                    f"beats {decision['reason']} "
                    f"{decision['confidence']:.0f}%)"
                )

        # ------------------------------------------
        # Step 3: build the final mapping
        # ------------------------------------------

        mapping = {}

        for field, decision in winners.items():

            mapping[decision["column"]] = field

            print(
                f"{decision['column']} ---> {field} "
                f"({decision['reason']}, {decision['confidence']:.0f}%)"
            )

        print("\n====================================\n")

        # Rename and keep mapped columns
        mapped_columns = list(mapping.keys())

        dataframe = dataframe[mapped_columns]

        dataframe = dataframe.rename(columns=mapping)

        duplicates = dataframe.columns[dataframe.columns.duplicated()]

        if len(duplicates):

            raise ValueError(
                f"Duplicate mapped columns detected: "
                f"{duplicates.tolist()}"
            )

        return dataframe
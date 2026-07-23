"""
CRDQE Value Matcher

Attempts to identify a column by looking at its values
instead of its header.

Pipeline

Header Match
    ↓
Alias Match
    ↓
Fuzzy Match
    ↓
Value Match
"""

from __future__ import annotations

from datetime import datetime
import pandas as pd


class ValueMatcher:

    SAMPLE_SIZE = 10
    MIN_CONFIDENCE = 80

    def __init__(self, schema):
        self.schema = schema

    def match(self, series):
        """
        Attempt to identify the schema field from sample values.

        Returns
        -------
        (field_name, confidence)

        field_name is None if no field scored high enough, OR if
        multiple fields tied for the best score -- a tie means the
        values themselves can't discriminate between those fields
        (e.g. every date-typed field scores identically against a
        plausible-looking date string), so it isn't confident,
        field-specific evidence and shouldn't be trusted over a
        header.
        """

        values = (
            series.dropna()
                  .astype(str)
                  .str.strip()
                  .head(self.SAMPLE_SIZE)
                  .tolist()
        )

        if not values:
            return None, 0

        scores = {}

        for field, rules in self.schema.items():

            score = self._score(values, rules)

            if score > 0:
                scores[field] = score

        if not scores:
            return None, 0

        best_score = max(scores.values())

        if best_score < self.MIN_CONFIDENCE:
            return None, best_score

        top_fields = [
            field
            for field, score in scores.items()
            if score == best_score
        ]

        if len(top_fields) > 1:
            return None, best_score

        return top_fields[0], best_score
    def _score(self, values, rules):

        datatype = rules.get("datatype")

        if "valid_values" in rules or "Valid_values" in rules:
            return self._score_enum(values, rules)

        if datatype in ("integer", "float"):
            return self._score_numeric(values, rules)

        if datatype == "date":
            return self._score_dates(values)

        return 0
    def _score_enum(self, values, rules):

        raw_valid = rules.get("valid_values") or rules.get("Valid_values") or {}

        valid = {
            k.lower()
            for k in raw_valid
        }

        hits = 0

        for value in values:

            if value.lower() in valid:
                hits += 1

        return round(hits / len(values) * 100)
    def _score_numeric(self, values, rules):

        minimum = rules.get("minimum", float("-inf"))
        maximum = rules.get("maximum", float("inf"))

        hits = 0

        for value in values:

            try:
                number = float(value)

                if minimum <= number <= maximum:
                    hits += 1

            except Exception:
                pass

        return round(hits / len(values) * 100)
    def _score_dates(self, values):

        formats = (
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%y",
            "%d/%m/%y",
        )

        hits = 0

        for value in values:

            parsed = False

            for fmt in formats:

                try:
                    datetime.strptime(value, fmt)
                    parsed = True
                    break

                except ValueError:
                    continue

            if parsed:
                hits += 1

        return round(hits / len(values) * 100)
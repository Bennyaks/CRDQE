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

        best_field = None
        best_score = 0

        for field, rules in self.schema.items():

            score = self._score(values, rules)

            if score > best_score:
                best_score = score
                best_field = field

        if best_score >= self.MIN_CONFIDENCE:
            return best_field, best_score

        return None, best_score
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
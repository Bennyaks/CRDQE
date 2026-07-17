"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Dataset Detector

Purpose:
Detect whether the workbook contains Birth or Death data.

Approach:
1. Primary signal: match each column header against every
   field's known aliases (and canonical name) in both the
   Birth and Death schemas. Whichever schema's aliases match
   more columns wins. This reuses the same alias lists that
   already drive column mapping, instead of a separate,
   hand-maintained keyword list that can silently drift out
   of sync (e.g. "sex" being claimed by both datasets).
2. Fallback: if the two schemas score too close to call
   (headers alone are ambiguous -- different workbook
   templates, unexpected wording, etc.), sample each column's
   actual cell values and check them against each schema's
   valid_values. Some values are dataset-specific by
   definition (e.g. "Born Alive"/"Born Dead" can only appear
   in Birth data), which makes this a strong tiebreaker even
   when headers don't help.
===========================================================
"""

from difflib import SequenceMatcher


ALIAS_MATCH_THRESHOLD = 0.85
TIE_MARGIN = 1


def _normalize(text):

    return str(text).strip().lower()


def _similarity(a, b):

    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


def _all_fields(schema):

    fields = {}

    fields.update(schema.get("source_columns", {}) or {})
    fields.update(schema.get("derived_columns", {}) or {})

    return fields


def _valid_values(details):

    # Schemas inconsistently use "valid_values" and "Valid_values" --
    # check both so detection doesn't silently miss a field.
    return (
        details.get("valid_values")
        or details.get("Valid_values")
        or {}
    )


class DatasetDetector:

    # ===========================================================
    # Header Alias Matching
    # ===========================================================

    @staticmethod
    def _score_headers(columns, schema):
        """
        Counts how many workbook columns closely match an alias
        (or canonical field name) defined in this schema.
        """

        fields = _all_fields(schema)

        score = 0

        for column in columns:

            best = 0

            for field, details in fields.items():

                candidates = [field] + list(details.get("aliases", []))

                for alias in candidates:

                    similarity = _similarity(column, alias)

                    if similarity > best:
                        best = similarity

            if best >= ALIAS_MATCH_THRESHOLD:
                score += 1

        return score

    # ===========================================================
    # Value Matching (fallback)
    # ===========================================================

    @staticmethod
    def _score_values(dataframe, schema):
        """
        Counts how many columns' actual values overlap with any
        field's valid_values defined in this schema. Used only
        when header matching alone is too close to call.
        """

        fields = _all_fields(schema)

        score = 0

        for column in dataframe.columns:

            try:

                values = (
                    dataframe[column]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .unique()
                )

            except Exception:
                continue

            values = set(values)

            if not values:
                continue

            for field, details in fields.items():

                valid = _valid_values(details)

                if not valid:
                    continue

                expected = {
                    str(v).strip().lower() for v in valid.values()
                } | {
                    str(k).strip().lower() for k in valid.keys()
                }

                if not expected:
                    continue

                overlap = len(values & expected) / len(expected)

                if overlap >= 0.5:
                    score += 1
                    break

        return score

    # ===========================================================
    # Detect
    # ===========================================================

    @staticmethod
    def detect(dataframe, birth_schema, death_schema):
        """
        Returns "Birth", "Death", or "Unknown".
        """

        columns = list(dataframe.columns)

        birth_header_score = DatasetDetector._score_headers(
            columns, birth_schema
        )

        death_header_score = DatasetDetector._score_headers(
            columns, death_schema
        )

        if abs(birth_header_score - death_header_score) > TIE_MARGIN:

            if birth_header_score > death_header_score:
                return "Birth"

            return "Death"

        # Header scores are too close -- fall back to values

        birth_value_score = DatasetDetector._score_values(
            dataframe, birth_schema
        )

        death_value_score = DatasetDetector._score_values(
            dataframe, death_schema
        )

        combined_birth = birth_header_score + birth_value_score
        combined_death = death_header_score + death_value_score

        if combined_birth > combined_death:
            return "Birth"

        elif combined_death > combined_birth:
            return "Death"

        return "Unknown"
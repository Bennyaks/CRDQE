"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Dataset Detector

Purpose:
Detect whether the workbook contains Birth or Death data.
===========================================================
"""


class DatasetDetector:

    BIRTH_KEYWORDS = [
        "birth",
        "date of birth",
        "weight",
        "mother",
        "born alive",
        "entry number",
    ]

    DEATH_KEYWORDS = [
        "death",
        "cause",
        "deceased",
        "burial",
        "age at death",
        "sex",
    ]

    @staticmethod
    def detect(columns):

        text = " ".join(str(c).lower() for c in columns)

        birth_score = sum(
            keyword in text
            for keyword in DatasetDetector.BIRTH_KEYWORDS
        )

        death_score = sum(
            keyword in text
            for keyword in DatasetDetector.DEATH_KEYWORDS
        )

        if birth_score > death_score:
            return "Birth"

        elif death_score > birth_score:
            return "Death"

        return "Unknown"
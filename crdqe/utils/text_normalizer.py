"""
Utility functions for normalizing text.
"""

import re


def normalize(text):
    """
    Normalize text for reliable comparisons.
    """

    text = str(text).lower()

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    text = text.replace(" (", "(")
    text = text.replace("( ", "(")
    text = text.replace(" )", ")")

    return text.strip()

import re


def normalize(text):
    """
    Normalize text for reliable comparisons.
    """

    text = str(text).lower()

    # Everything after "(" is usually explanatory text.
    text = text.split("(")[0]

    text = text.replace("\n", " ")

    text = re.sub(r"[_/-]", " ", text)

    text = re.sub(r"[^a-z0-9\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
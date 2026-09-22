import re


def normalize_text(text):
    """
    Normalize whitespace so transcript text can
    be compared reliably.
    """

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def validate_evidence(evidence):
    """
    Validate that each evidence record contains
    the required source metadata.

    Also normalizes whitespace in the displayed
    evidence text without changing its meaning.
    """

    validated = []

    required_fields = [
        "country",
        "expert",
        "role",
        "timestamp",
        "question_number",
        "text"
    ]

    for item in evidence:

        missing_fields = [
            field
            for field in required_fields
            if not item.get(field)
        ]

        cleaned_item = {
            **item,
            "text": normalize_text(
                item.get("text", "")
            )
        }

        if missing_fields:

            validated.append({
                **cleaned_item,
                "valid": False,
                "error": (
                    "Missing fields: "
                    + ", ".join(missing_fields)
                )
            })

        else:

            validated.append({
                **cleaned_item,
                "valid": True,
                "error": None
            })

    return validated


def quote_exists(source_text, quote):
    """
    Check whether a quote exists in the source text
    after whitespace normalization.
    """

    source = normalize_text(
        source_text
    )

    candidate = normalize_text(
        quote
    )

    return candidate in source
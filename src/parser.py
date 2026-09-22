import re
from pathlib import Path


EXPERT_METADATA = {
    "France": {
        "expert": "Dr. Jean Martin",
        "role": "Head of Urology"
    },
    "Germany": {
        "expert": "Anna Keller",
        "role": "Former Hospital Procurement Director"
    },
    "United Kingdom": {
        "expert": "Dr. Emily Carter",
        "role": "Consultant Urologist"
    }
}


def parse_transcript(file_path: str, country: str):
    """Parse transcript into structured expert evidence."""

    text = Path(file_path).read_text(
        encoding="utf-8-sig"
    )

    timestamp_pattern = r"\b(\d{2}:\d{2})\b"

    matches = list(
        re.finditer(
            timestamp_pattern,
            text
        )
    )

    metadata = EXPERT_METADATA.get(
        country,
        {}
    )

    segments = []

    question_number = 0

    for i, match in enumerate(matches):

        timestamp = match.group(1)

        start = match.end()

        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(text)
        )

        block = text[start:end].strip()

        if not block:
            continue

        block = (
            block
            .replace("\u200b", "")
            .replace("\ufeff", "")
            .strip()
        )

        if ":" not in block:
            continue

        speaker, dialogue = block.split(
            ":",
            1
        )

        speaker = speaker.strip()
        dialogue = dialogue.strip()

        # Interviewer starts a new interview question
        if speaker.lower().startswith(
            "interviewer"
        ):
            question_number += 1
            continue

        # Ignore anything before the first question
        if question_number == 0:
            continue

        segments.append({
            "country": country,
            "expert": metadata.get(
                "expert",
                speaker
            ),
            "role": metadata.get(
                "role",
                ""
            ),
            "question_number": question_number,
            "timestamp": timestamp,
            "speaker": speaker,
            "text": dialogue
        })

    return segments
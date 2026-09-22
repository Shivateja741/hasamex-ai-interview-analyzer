from src.parser import parse_transcript
from src.retrieval import EvidenceRetriever
from src.validation import validate_evidence


files = [
    (
        "data/Transcript_1_France.txt",
        "France"
    ),
    (
        "data/Transcript_2_Germany.txt",
        "Germany"
    ),
    (
        "data/Transcript_3_UK.txt",
        "United Kingdom"
    ),
]


all_segments = []


for file_path, country in files:

    segments = parse_transcript(
        file_path,
        country
    )

    all_segments.extend(segments)


retriever = EvidenceRetriever(
    all_segments
)


question = "What are the main barriers to adoption?"


evidence = retriever.search(
    query=question,
    top_k=3,
    question_number=2
)


validated = validate_evidence(
    evidence
)


print("\nEVIDENCE VALIDATION\n")


for item in validated:

    print(
        f"Country: {item['country']}"
    )

    print(
        f"Expert: {item['expert']}"
    )

    print(
        f"Timestamp: {item['timestamp']}"
    )

    print(
        f"Question: Q{item['question_number']}"
    )

    print(
        f"Valid: {item['valid']}"
    )

    if item["error"]:
        print(
            f"Error: {item['error']}"
        )

    print(
        f"Quote: {item['text']}"
    )

    print("-" * 80)
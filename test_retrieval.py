from src.parser import parse_transcript
from src.retrieval import EvidenceRetriever


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


print(
    f"Loaded {len(all_segments)} expert responses."
)


retriever = EvidenceRetriever(
    all_segments
)


query = "What are the main barriers to adoption?"


results = retriever.search(
    query=query,
    top_k=3,
    question_number=2
)


print("\nQUERY:")
print(query)

print("\nTOP EVIDENCE:\n")


for result in results:

    print(
        f"{result['country']} | "
        f"{result['expert']} | "
        f"{result['role']}"
    )

    print(
        f"Question: Q{result['question_number']}"
    )

    print(
        f"Timestamp: {result['timestamp']}"
    )

    print(
        f"Score: {result['score']:.3f}"
    )

    print(
        f"Quote: {result['text']}"
    )

    print("-" * 80)
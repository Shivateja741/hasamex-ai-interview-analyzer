from src.parser import parse_transcript
from src.retrieval import EvidenceRetriever
from src.llm import LLMClient


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


question = "What are the main barriers to adoption?"


evidence = retriever.search(
    query=question,
    top_k=3,
    question_number=2
)


llm = LLMClient()


result = llm.answer(
    question,
    evidence
)


print("\nQUESTION:")
print(question)


print("\nANSWER:")
print(result["answer"])


print("\nCOMMON THEMES:")

for theme in result["common_themes"]:

    print(
        f"- {theme}"
    )


print("\nMARKET DIFFERENCES:")

for difference in result["market_differences"]:

    print(
        f"- {difference['market']}: "
        f"{difference['difference']}"
    )


print("\nSOURCE EVIDENCE:")


for item in evidence:

    print(
        f"\n{item['country']} | "
        f"{item['expert']} | "
        f"{item['timestamp']}"
    )

    print(item["text"])
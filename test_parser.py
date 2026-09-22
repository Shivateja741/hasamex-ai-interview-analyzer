from src.parser import parse_transcript


files = [
    ("data/Transcript_1_France.txt", "France"),
    ("data/Transcript_2_Germany.txt", "Germany"),
    ("data/Transcript_3_UK.txt", "United Kingdom"),
]


all_segments = []

for file_path, country in files:
    segments = parse_transcript(file_path, country)
    all_segments.extend(segments)

    print(f"{country}: {len(segments)} expert responses")


print(f"\nTotal expert responses: {len(all_segments)}")

print("\nFirst 5 evidence records:\n")

for segment in all_segments[:5]:
    print(segment)
    print("-" * 80)
import os
import json
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMClient:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"


    def answer(self, question, evidence):

        # -----------------------------------------
        # Build evidence context
        # -----------------------------------------

        evidence_text = ""

        for i, item in enumerate(evidence, 1):

            evidence_text += f"""
Evidence {i}
Country: {item["country"]}
Expert: {item["expert"]}
Role: {item["role"]}
Timestamp: {item["timestamp"]}
Question: Q{item["question_number"]}
Source text: {item["text"]}
"""


        # -----------------------------------------
        # Structured research prompt
        # -----------------------------------------

        prompt = f"""
You are a senior qualitative market research analyst.

Analyze the expert interview evidence below.

USER QUESTION:
{question}

EVIDENCE:
{evidence_text}

IMPORTANT RULES:

1. Use ONLY the supplied evidence.

2. Do not invent facts, statistics, quotes,
   timestamps, experts, or countries.

3. Identify themes that are actually supported
   by multiple pieces of evidence.

4. Clearly describe market-specific differences.

5. Do not call something a disagreement unless
   experts actually contradict each other.

6. Do not create or modify direct quotations.

7. The source evidence will be displayed separately,
   so do not include long direct quotations in the answer.

8. If evidence is insufficient, say so explicitly.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "answer": "A concise synthesis answering the question.",
    "common_themes": [
        "Theme supported by the evidence"
    ],
    "market_differences": [
        {{
            "market": "Country",
            "difference": "What this expert emphasized"
        }}
    ]
}}
"""


        # -----------------------------------------
        # Call Groq
        # -----------------------------------------

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise, evidence-grounded "
                        "qualitative research analyst. "
                        "Return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }
        )


        # -----------------------------------------
        # Parse JSON
        # -----------------------------------------

        content = response.choices[0].message.content

        try:

            result = json.loads(content)

        except json.JSONDecodeError:

            return {
                "answer": content,
                "common_themes": [],
                "market_differences": []
            }


        return result
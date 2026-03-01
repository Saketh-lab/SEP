import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_pitch(transcript: str, examples: list) -> dict:
    examples_str = json.dumps(examples[:5], indent=2)

    prompt = f"""
You are a YC partner evaluating startup pitches.

Here are 5 example YC-funded startups for reference:
{examples_str}

Now evaluate this pitch transcript:
\"\"\"
{transcript}
\"\"\"

Score 1-5 on each dimension. Be specific in your reasoning.
Use the YC examples above as your benchmark — a 5 means comparable to those companies at their stage.

Return ONLY valid JSON with no extra text, markdown, or explanation:
{{
  "scores": {{
    "founder_signal": <1-5>,
    "problem_clarity": <1-5>,
    "traction": <1-5>,
    "market_size": <1-5>,
    "overall": <1-5>
  }},
  "reasoning": {{
    "founder_signal": "<why>",
    "problem_clarity": "<why>",
    "traction": "<why>",
    "market_size": "<why>",
    "overall": "<summary>"
  }},
  "most_similar_yc_company": "<name>",
  "red_flags": ["<flag1>", "<flag2>"],
  "strengths": ["<strength1>", "<strength2>"]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if model wraps response in them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def pick_relevant_examples(transcript: str, examples: list, n: int = 5) -> list:
    """
    Simple keyword-based relevance filter to pick the most relevant
    YC examples for a given pitch. Falls back to first n if no matches.
    """
    transcript_lower = transcript.lower()

    def relevance_score(example):
        text = (example.get("problem", "") + " " + example.get("market", "")).lower()
        words = set(transcript_lower.split())
        return sum(1 for word in words if len(word) > 4 and word in text)

    scored = sorted(examples, key=relevance_score, reverse=True)
    return scored[:n]


def safe_evaluate(transcript: str, examples: list, retries: int = 2) -> dict:
    relevant_examples = pick_relevant_examples(transcript, examples)

    for i in range(retries):
        try:
            return evaluate_pitch(transcript, relevant_examples)
        except json.JSONDecodeError:
            if i == retries - 1:
                return {"error": "Could not parse evaluation — the model returned malformed JSON. Please try again."}
        except Exception as e:
            if i == retries - 1:
                return {"error": f"Groq API error: {str(e)}"}
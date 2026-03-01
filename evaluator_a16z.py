import openai
import json
import os

def evaluate_pitch_a16z(transcript: str, examples: list) -> dict:
    """
    Evaluate a startup pitch using a16z's investment framework.
    
    a16z looks for: bold technical vision, network effects, category-defining companies,
    contrarian insights, and founders who can articulate a compelling future.
    """
    examples_str = json.dumps(examples[:5], indent=2)
    
    prompt = f"""
You are an a16z (Andreessen Horowitz) partner evaluating startup pitches.

a16z's investment philosophy:
- "Software is eating the world" - back bold technical visions
- Strong preference for network effects and platform businesses
- Invest in contrarian insights that seem crazy but might be right
- Value founder vision and ability to articulate a compelling future
- Portfolio support matters - companies that benefit from a16z network

Here are 5 example a16z portfolio companies for reference:
{examples_str}

Now evaluate this pitch transcript:
\"\"\"
{transcript}
\"\"\"

Score 1-5 on each dimension using a16z's bar (5 = portfolio-ready).

Return ONLY valid JSON (no markdown, no preamble):
{{
  "scores": {{
    "technical_vision": <1-5>,
    "network_effects": <1-5>,
    "contrarian_insight": <1-5>,
    "founder_conviction": <1-5>,
    "platform_potential": <1-5>,
    "overall": <1-5>
  }},
  "reasoning": {{
    "technical_vision": "<why - is this a bold technical bet?>",
    "network_effects": "<why - does this get stronger as it grows?>",
    "contrarian_insight": "<why - is this a non-obvious truth?>",
    "founder_conviction": "<why - can they paint a compelling future?>",
    "platform_potential": "<why - can this become infrastructure?>",
    "overall": "<investment decision summary>"
  }},
  "most_similar_a16z_company": "<name>",
  "investment_stage": "<Seed|Series A|Series B|Growth|Not ready>",
  "concerns": ["<concern1>", "<concern2>"],
  "strengths": ["<strength1>", "<strength2>"],
  "a16z_thesis": "<1-2 sentence investment thesis if a16z would invest>",
  "portfolio_fit": "<how this company benefits from a16z network - specific connections/intros/expertise>"
}}
"""
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    content = response.choices[0].message.content.strip()
    
    # Remove markdown code fences if present
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    
    return json.loads(content.strip())


def safe_evaluate_a16z(transcript: str, examples: list, retries: int = 2) -> dict:
    """Wrapper with retry logic for JSON parsing errors."""
    for i in range(retries):
        try:
            return evaluate_pitch_a16z(transcript, examples)
        except json.JSONDecodeError as e:
            if i == retries - 1:
                return {
                    "error": "Could not parse evaluation",
                    "details": str(e),
                    "scores": {
                        "technical_vision": 0,
                        "network_effects": 0,
                        "contrarian_insight": 0,
                        "founder_conviction": 0,
                        "platform_potential": 0,
                        "overall": 0
                    }
                }
    return {"error": "Unexpected error"}

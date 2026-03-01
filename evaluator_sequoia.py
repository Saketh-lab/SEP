import openai
import json
import os
import time
from dotenv import load_dotenv

# Load .env from the same folder as this file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise EnvironmentError(
        "\n\n❌ GROQ_API_KEY not found!\n"
        "Please create a .env file in the same folder as this script with:\n\n"
        "    GROQ_API_KEY=gsk_your-key-here\n\n"
        "Get your free key at: https://console.groq.com\n"
    )

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)


def evaluate_pitch_sequoia(transcript: str, examples: list) -> dict:
    """
    Evaluate a startup pitch transcript using Sequoia Capital's investment framework.
    
    Args:
        transcript: The pitch transcript text to evaluate
        examples: List of Sequoia portfolio company examples for few-shot context
    
    Returns:
        dict: Structured evaluation with scores, reasoning, and recommendations
    """
    # Use a diverse sample of 5 companies across different stages and sectors
    example_sample = _select_diverse_examples(examples, n=5)
    examples_str = json.dumps(example_sample, indent=2)

    prompt = f"""You are a Sequoia Capital partner evaluating startup pitches.

Sequoia looks for: enduring companies, market leadership potential, technical moats, 
strong unit economics, and founders who can scale from 10 to 10,000 people.

Sequoia's core investment thesis pillars:
1. Back companies that can be the last-standing player in a large, important market
2. Invest in technical or data moats that compound over time and resist competition
3. Founders who combine visionary thinking with brutal operational execution
4. Business models with strong unit economics and a clear path to 70%+ gross margins
5. Category creators who define new markets rather than compete in existing ones

Here are 5 example Sequoia portfolio companies for reference context:
{examples_str}

Now evaluate this pitch transcript:
\"\"\"
{transcript}
\"\"\"

Score each dimension 1–5 using Sequoia's bar (5 = portfolio-ready, 3 = interesting but not there yet, 1 = pass):

Return ONLY valid JSON with no additional text, markdown, or explanation:
{{
  "scores": {{
    "market_leadership": <1-5>,
    "technical_moat": <1-5>,
    "unit_economics": <1-5>,
    "founder_scaling": <1-5>,
    "category_creation": <1-5>,
    "overall": <1-5>
  }},
  "reasoning": {{
    "market_leadership": "<2-3 sentences: can this be unambiguous #1 in its category? what evidence supports or undermines this?>",
    "technical_moat": "<2-3 sentences: what makes this defensible? is the moat technical, data-driven, network-based, or regulatory?>",
    "unit_economics": "<2-3 sentences: what are the current margins? what's the path to 70%+ gross margins and strong LTV/CAC?>",
    "founder_scaling": "<2-3 sentences: evidence the founders can hire executives, delegate, and build an organization of 1000+ people?>",
    "category_creation": "<2-3 sentences: is this a new market, a displacement play, or a horizontal platform? how large could the category become?>",
    "overall": "<3-4 sentence investment decision summary — would Sequoia write the check? what's the bull case and bear case?>"
  }},
  "most_similar_sequoia_company": "<name of the closest portfolio company analog and why>",
  "investment_stage": "<Seed|Series A|Series B|Growth|Not ready>",
  "concerns": [
    "<specific concern 1 with context>",
    "<specific concern 2 with context>",
    "<specific concern 3 with context>"
  ],
  "strengths": [
    "<specific strength 1 with evidence from the pitch>",
    "<specific strength 2 with evidence from the pitch>",
    "<specific strength 3 with evidence from the pitch>"
  ],
  "sequoia_lens": "<2-3 sentence investment thesis written as if a Sequoia partner were presenting this to their Monday meeting. Be specific about why Sequoia specifically — not just any VC — would want to lead this round.>",
  "next_milestones": [
    "<key milestone 1 that would unlock the next funding round>",
    "<key milestone 2 that would prove out the core thesis>",
    "<key milestone 3 that would de-risk the biggest concern>"
  ]
}}"""

    # Retry up to 3 times with backoff for rate limit errors
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
            )
            break
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait = 60 * (attempt + 1)
                print(f"Rate limit hit, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise e

    raw_content = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if raw_content.startswith("```"):
        raw_content = raw_content.split("```")[1]
        if raw_content.startswith("json"):
            raw_content = raw_content[4:]
        raw_content = raw_content.strip()

    try:
        result = json.loads(raw_content)
    except json.JSONDecodeError as e:
        # Return a structured error response
        result = {
            "scores": {
                "market_leadership": 0,
                "technical_moat": 0,
                "unit_economics": 0,
                "founder_scaling": 0,
                "category_creation": 0,
                "overall": 0,
            },
            "reasoning": {
                "market_leadership": "Error parsing evaluation",
                "technical_moat": "Error parsing evaluation",
                "unit_economics": "Error parsing evaluation",
                "founder_scaling": "Error parsing evaluation",
                "category_creation": "Error parsing evaluation",
                "overall": f"JSON parse error: {str(e)}. Raw response: {raw_content[:500]}",
            },
            "most_similar_sequoia_company": "Unknown",
            "investment_stage": "Error",
            "concerns": ["Evaluation failed due to parsing error"],
            "strengths": [],
            "sequoia_lens": "Evaluation failed",
            "next_milestones": [],
        }

    return result


def _select_diverse_examples(examples: list, n: int = 5) -> list:
    """
    Select a diverse set of examples across stages and sectors for better few-shot context.
    """
    if len(examples) <= n:
        return examples

    # Try to get diversity across stages
    stages = {}
    for ex in examples:
        stage = ex.get("stage_at_investment", "Unknown")
        if stage not in stages:
            stages[stage] = []
        stages[stage].append(ex)

    selected = []
    stage_order = ["Seed / Series A equivalent", "Series A", "Series B", "Growth", "Unknown"]

    for stage in stage_order:
        if stage in stages and len(selected) < n:
            selected.append(stages[stage][0])

    # Fill remaining slots
    for ex in examples:
        if len(selected) >= n:
            break
        if ex not in selected:
            selected.append(ex)

    return selected[:n]


def batch_evaluate(transcripts: list, examples: list) -> list:
    """
    Evaluate multiple pitch transcripts in batch.
    
    Args:
        transcripts: List of (name, transcript) tuples
        examples: List of Sequoia portfolio examples
    
    Returns:
        List of (name, evaluation) tuples
    """
    results = []
    for name, transcript in transcripts:
        print(f"Evaluating: {name}")
        result = evaluate_pitch_sequoia(transcript, examples)
        results.append((name, result))
    return results

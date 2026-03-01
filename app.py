import gradio as gr
import json
import os
from evaluator import safe_evaluate

# Load YC examples once at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "yc_examples.json")) as f:
    YC_EXAMPLES = json.load(f)

# Sample pitches for the demo button
SAMPLE_STRONG = """
Hi, I'm Sarah Chen, ex-Google engineer and former logistics manager at Amazon.
We're building FreightFlow — an API that lets e-commerce companies get real-time 
freight quotes and book shipments in under 60 seconds, compared to the industry 
standard of 2-3 days.

We've been live for 4 months. We're processing $800K in monthly freight volume, 
growing 40% month over month. We have 12 paying customers including two $10M+ 
e-commerce brands who came to us through word of mouth.

The US freight brokerage market is $100B. It runs almost entirely on phone calls 
and email. We're the Stripe for freight — one API call, instant quote, instant booking.
"""

SAMPLE_WEAK = """
We're building an app that helps people find restaurants. There are a lot of 
restaurants out there and people don't always know where to go. Our app will 
use AI to recommend places based on your mood.

We just started working on this last month. We have a prototype but no users yet.
The restaurant industry is really big, like hundreds of billions of dollars.
We think if we get 1% of the market that would be amazing.
"""


def format_stars(score: int) -> str:
    return "⭐" * score + "☆" * (5 - score)


def run_evaluation(pitch_text: str):
    if not pitch_text.strip():
        return "⚠️ Please enter a pitch transcript.", "{}"

    result = safe_evaluate(pitch_text, YC_EXAMPLES)

    if "error" in result:
        return f"⚠️ {result['error']}", "{}"

    scores = result["scores"]
    reasoning = result["reasoning"]

    overall_score = scores["overall"]
    if overall_score >= 4:
        verdict = "🟢 Strong pitch — YC-competitive"
    elif overall_score == 3:
        verdict = "🟡 Promising — needs work in key areas"
    else:
        verdict = "🔴 Early stage — significant gaps to address"

    display = f"""
## {verdict}

---

## Scores

| Dimension | Score | Rating |
|-----------|-------|--------|
| Founder Signal | {scores['founder_signal']}/5 | {format_stars(scores['founder_signal'])} |
| Problem Clarity | {scores['problem_clarity']}/5 | {format_stars(scores['problem_clarity'])} |
| Traction | {scores['traction']}/5 | {format_stars(scores['traction'])} |
| Market Size | {scores['market_size']}/5 | {format_stars(scores['market_size'])} |
| **Overall** | **{scores['overall']}/5** | **{format_stars(scores['overall'])}** |

---

## Most Similar YC Company
🏢 **{result['most_similar_yc_company']}**

---

## Strengths
{chr(10).join("✅ " + s for s in result['strengths'])}

## Red Flags
{chr(10).join("🚩 " + f for f in result['red_flags'])}

---

## Detailed Reasoning

**Founder Signal:** {reasoning['founder_signal']}

**Problem Clarity:** {reasoning['problem_clarity']}

**Traction:** {reasoning['traction']}

**Market Size:** {reasoning['market_size']}

**Overall:** {reasoning['overall']}
"""

    return display, json.dumps(result, indent=2)


def load_sample(sample_type: str):
    if sample_type == "strong":
        return SAMPLE_STRONG.strip()
    return SAMPLE_WEAK.strip()


# --- UI Layout ---
with gr.Blocks(theme=gr.themes.Soft(), title="YC Pitch Evaluator") as demo:
    gr.Markdown("""
    # 🚀 YC Pitch Evaluator
    Evaluate your startup pitch against 20 YC-funded companies. Paste a transcript or use a sample pitch.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            pitch_input = gr.Textbox(
                lines=18,
                placeholder="Paste your pitch transcript here...\n\nTip: Include who you are, what you're building, the problem, your traction, and your market size.",
                label="Pitch Transcript"
            )

            with gr.Row():
                sample_strong_btn = gr.Button("📋 Load Strong Sample", variant="secondary", size="sm")
                sample_weak_btn = gr.Button("📋 Load Weak Sample", variant="secondary", size="sm")

            evaluate_btn = gr.Button("Evaluate Pitch →", variant="primary", size="lg")

        with gr.Column(scale=1):
            eval_output = gr.Markdown(label="Evaluation", value="*Your evaluation will appear here...*")

    with gr.Accordion("Raw JSON Output", open=False):
        json_output = gr.Code(language="json", label="Raw JSON")

    # Event handlers
    evaluate_btn.click(
        fn=run_evaluation,
        inputs=[pitch_input],
        outputs=[eval_output, json_output]
    )

    sample_strong_btn.click(
        fn=lambda: load_sample("strong"),
        outputs=[pitch_input]
    )

    sample_weak_btn.click(
        fn=lambda: load_sample("weak"),
        outputs=[pitch_input]
    )

    gr.Markdown("""
    ---
    *Benchmarked against 20 YC companies including Stripe, Airbnb, DoorDash, Brex, Scale AI, and more.*
    """)


if __name__ == "__main__":
    demo.launch(share=False)
import gradio as gr
import json
import os
from evaluator_sequoia import evaluate_pitch_sequoia

# Load portfolio examples
with open(os.path.join(os.path.dirname(__file__), "sequoia_examples.json")) as f:
    SEQUOIA_EXAMPLES = json.load(f)

# ─────────────────────────────────────────
# Sample pitches for quick testing
# ─────────────────────────────────────────

SAMPLE_PITCHES = {
    "Synthflow (AI Voice — Strong)": """
We're building Synthflow, an AI voice agent platform for enterprises.

Problem: Customer service costs $50B/year in the US alone. Hiring, training, and retaining 
call center agents is expensive and slow. Quality is inconsistent across reps, shifts, and 
languages. Enterprise NPS for phone support averages -11.

Solution: AI voice agents that sound human, handle complex multi-turn conversations, and 
integrate natively with existing CRM systems. We use our own proprietary speech models 
(not OpenAI or ElevenLabs) achieving 180ms latency and $0.02/minute costs vs $1.20+ for 
human agents. Our agents handle 94% of calls without escalation.

Traction: $420K MRR growing 30% MoM, 14 enterprise customers (average $36K ACV). 
87% gross margins. Customers report 62% cost reduction vs human agents. 
Net revenue retention: 143% — customers expand to new call center functions within 90 days.
3 Fortune 500 companies in late-stage pilots.

Market: Global call center market is $500B. We're starting with SMB and mid-market 
customer service, then expanding to enterprise sales calls and internal IT helpdesks. 
Our 3-year path gets us to 15% of the US mid-market — $8B TAM.

Team: CEO previously scaled engineering at Twilio from 40 to 400 engineers. 
CTO built Stripe's voice fraud detection system. We have 11 people, 8 engineers. 
Raised $3M seed from Kleiner Perkins 10 months ago. 2 pending patents on our 
real-time speaker diarization model.

Raising $12M Series A to double GTM team and expand to European mid-market.
""",

    "EcoTrack (Climate — Too Early)": """
Hi, we're EcoTrack. We help people track their carbon footprint.

Problem: Climate change is bad and people don't know how much carbon they emit.

Solution: Our app lets you log your activities and we calculate your carbon footprint. 
You get tips on how to reduce it. We also have a social feature so you can compare 
with friends.

Traction: We launched 3 months ago and have 2,000 downloads. About 400 people 
used it more than once. We haven't monetized yet but we're thinking about a $4.99/month 
premium plan or selling anonymized data.

Market: Everyone cares about climate. There are 8 billion people on Earth. 
Even if we got 1% that's 80 million users.

Team: I'm a recent CS grad passionate about sustainability. My co-founder is 
studying environmental science. We're pre-revenue and looking to raise $500K 
to hire a marketing person and improve the app.
""",

    "DataMesh (Enterprise Data — Growth Stage)": """
DataMesh is the leading data mesh infrastructure platform for Fortune 500 companies.

Problem: Large enterprises have data scattered across 50-200 internal data sources. 
Central data teams create bottlenecks — 6-18 month wait times for data products. 
Business teams can't access data they need; data engineers are overwhelmed.

Solution: DataMesh enables domain-driven data ownership — each business unit owns and 
publishes its data as a product using our standardized platform. Central governance 
layer enforces quality, security, and compliance automatically.

Traction: $28M ARR growing 85% YoY. 45 enterprise customers including 6 of the 
Fortune 50. Average ACV $620K. 158% net dollar retention — customers add 3-5 domains 
per year after initial deployment. $0 churn in 24 months. 
92% gross margins on software (excluding PS).

Market: Data management and governance $18B growing to $55B by 2028. 
Our ICP is enterprises with 5,000+ employees — 3,200 companies globally.
We've penetrated 1.4% of TAM.

Team: CEO previously GM of Databricks' enterprise business ($800M ARR division).
CTO was founding engineer at Palantir. 85 employees, 60% technical.
Backed by Accel and Bessemer ($42M raised to date).

Raising $60M Series C for international expansion (EMEA and APAC) and 
to accelerate our AI data product layer.
"""
}

# ─────────────────────────────────────────
# Scoring helper
# ─────────────────────────────────────────

SCORE_EMOJI = {5: "🟢", 4: "🟡", 3: "🟠", 2: "🔴", 1: "⛔"}
STARS = lambda n: "⭐" * n + "☆" * (5 - n)

DIMENSION_DESCRIPTIONS = {
    "market_leadership": "Can this be #1 in category?",
    "technical_moat": "Is this defensible?",
    "unit_economics": "Path to strong margins?",
    "founder_scaling": "Can they build a 1000+ person company?",
    "category_creation": "New market or displacing incumbent?",
}


def score_bar(score: int) -> str:
    filled = "█" * score
    empty = "░" * (5 - score)
    return f"`{filled}{empty}` {score}/5"


def run_evaluation(pitch_text: str) -> tuple[str, str]:
    """Main evaluation function called by Gradio."""
    if not pitch_text or len(pitch_text.strip()) < 50:
        return (
            "⚠️ Please provide a pitch transcript of at least a few sentences.",
            "{}",
        )

    try:
        result = evaluate_pitch_sequoia(pitch_text, SEQUOIA_EXAMPLES)
    except Exception as e:
        return (
            f"❌ Evaluation failed: {str(e)}\n\nPlease check your Groq API key in the `.env` file.",
            "{}",
        )

    scores = result.get("scores", {})
    reasoning = result.get("reasoning", {})
    overall_score = scores.get("overall", 0)
    overall_emoji = SCORE_EMOJI.get(overall_score, "❓")

    # Investment verdict banner
    if overall_score >= 4:
        verdict = "🟢 **STRONG INTEREST — Sequoia would likely move to partner meeting**"
    elif overall_score == 3:
        verdict = "🟡 **INTERESTING — Needs work on key dimensions before Series A**"
    elif overall_score == 2:
        verdict = "🟠 **PASS FOR NOW — Strong concerns; revisit at next milestone**"
    else:
        verdict = "⛔ **PASS — Not ready for institutional investment at this stage**"

    # Stage badge
    stage = result.get("investment_stage", "Unknown")
    stage_colors = {
        "Seed": "🌱",
        "Series A": "🚀",
        "Series B": "📈",
        "Growth": "🏢",
        "Not ready": "⚠️",
        "Error": "❌",
    }
    stage_icon = stage_colors.get(stage, "📋")

    # Build score table
    score_rows = ""
    for dim, desc in DIMENSION_DESCRIPTIONS.items():
        s = scores.get(dim, 0)
        emoji = SCORE_EMOJI.get(s, "❓")
        score_rows += f"| {dim.replace('_', ' ').title()} | {STARS(s)} | {emoji} {s}/5 | {desc} |\n"

    # Strengths and concerns
    strengths_md = "\n".join(
        f"✅ {s}" for s in result.get("strengths", ["No strengths identified"])
    )
    concerns_md = "\n".join(
        f"⚠️ {c}" for c in result.get("concerns", ["No concerns identified"])
    )

    # Next milestones
    milestones = result.get("next_milestones", [])
    milestones_md = ""
    if milestones:
        milestones_md = "\n---\n\n## 🎯 Key Milestones to Unlock Next Round\n"
        for i, m in enumerate(milestones, 1):
            milestones_md += f"\n**{i}.** {m}"

    # Detailed reasoning
    reasoning_md = ""
    dim_icons = {
        "market_leadership": "🏆",
        "technical_moat": "🛡️",
        "unit_economics": "💰",
        "founder_scaling": "👥",
        "category_creation": "🌐",
        "overall": "📋",
    }
    for dim, icon in dim_icons.items():
        if dim in reasoning:
            label = dim.replace("_", " ").title()
            reasoning_md += f"\n**{icon} {label}:** {reasoning[dim]}\n"

    score_display = f"""# 🌲 Sequoia Investment Evaluation

## {overall_emoji} Overall Verdict
{verdict}

**Investment Stage:** {stage_icon} {stage} &nbsp;&nbsp;|&nbsp;&nbsp; **Closest Comp:** 🏢 {result.get("most_similar_sequoia_company", "Unknown")}

---

## 📊 Scorecard

| Dimension | Rating | Score | Sequoia Question |
|-----------|--------|-------|-----------------|
{score_rows}
| **Overall** | {STARS(overall_score)} | **{overall_emoji} {overall_score}/5** | **Investment decision** |

---

## 💡 Sequoia Investment Thesis
> {result.get("sequoia_lens", "Not ready for institutional investment at current stage.")}

---

## ✅ Strengths
{strengths_md}

## ⚠️ Key Concerns
{concerns_md}
{milestones_md}

---

## 🔍 Detailed Reasoning
{reasoning_md}

---
*Evaluated against {len(SEQUOIA_EXAMPLES)} Sequoia portfolio companies across Seed through Growth stages.*
"""

    return score_display, json.dumps(result, indent=2)


def load_sample(sample_name: str) -> str:
    """Load a sample pitch by name."""
    return SAMPLE_PITCHES.get(sample_name, "")


# ─────────────────────────────────────────
# Gradio UI
# ─────────────────────────────────────────

with gr.Blocks(
    title="🌲 Sequoia Pitch Evaluator",
    theme=gr.themes.Soft(
        primary_hue="emerald",
        secondary_hue="teal",
        font=gr.themes.GoogleFont("Inter"),
    ),
    css="""
    .header-box { background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%); 
                  padding: 2rem; border-radius: 12px; margin-bottom: 1rem; }
    .header-box h1 { color: white; margin: 0; font-size: 2rem; }
    .header-box p  { color: #a7f3d0; margin: 0.5rem 0 0 0; }
    .sample-label  { font-weight: 600; color: #065f46; }
    footer { display: none !important; }
    """,
) as demo:
    
    gr.HTML("""
    <div class="header-box">
      <h1>🌲 Sequoia Pitch Evaluator</h1>
      <p>Evaluate your startup pitch using Sequoia Capital's investment framework — 
         backed by analysis of 28 iconic portfolio companies.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Quick Load Sample Pitch", elem_classes=["sample-label"])
            sample_selector = gr.Dropdown(
                choices=list(SAMPLE_PITCHES.keys()),
                label="Load a sample pitch",
                value=None,
                interactive=True,
            )
            load_btn = gr.Button("📥 Load Sample", variant="secondary", size="sm")

        with gr.Column(scale=3):
            pass

    pitch_input = gr.Textbox(
        lines=18,
        placeholder="""Paste your pitch transcript here. Include:
• Problem — what pain are you solving and for whom?
• Solution — your product/technology approach
• Traction — revenue, growth, customer metrics  
• Market — TAM and your wedge into it
• Team — founder backgrounds and relevant experience
• Ask — how much you're raising and what for

The more detail you provide, the more precise your evaluation will be.""",
        label="Pitch Transcript",
        show_label=True,
    )

    with gr.Row():
        evaluate_btn = gr.Button(
            "🌲 Evaluate with Sequoia Framework", variant="primary", size="lg", scale=3
        )
        clear_btn = gr.Button("🗑️ Clear", variant="secondary", size="lg", scale=1)

    with gr.Row():
        eval_output = gr.Markdown(
            label="Sequoia Evaluation",
            value="*Your evaluation will appear here after submission...*",
        )

    with gr.Accordion("🔩 Raw JSON Output", open=False):
        json_output = gr.Code(label="Structured Evaluation Data", language="json")

    # ── Event handlers ──────────────────────────────────────────────
    evaluate_btn.click(
        fn=run_evaluation,
        inputs=[pitch_input],
        outputs=[eval_output, json_output],
        api_name="evaluate",
    )

    load_btn.click(fn=load_sample, inputs=[sample_selector], outputs=[pitch_input])

    clear_btn.click(
        fn=lambda: ("", "*Your evaluation will appear here after submission...*", ""),
        outputs=[pitch_input, eval_output, json_output],
    )

    gr.Markdown("""
---
**Evaluation Dimensions:** Market Leadership · Technical Moat · Unit Economics · Founder Scaling · Category Creation

Built on analysis of 28 Sequoia portfolio companies including Stripe, Airbnb, Zoom, Snowflake, Figma, and more.
*This tool is for educational purposes and does not represent official Sequoia Capital views.*
""")


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
    )

import gradio as gr
import json
from evaluator_a16z import safe_evaluate_a16z

# Load a16z portfolio examples
with open("a16z_examples.json") as f:
    A16Z_EXAMPLES = json.load(f)

def run_evaluation(pitch_text):
    """Evaluate a pitch using a16z framework."""
    result = safe_evaluate_a16z(pitch_text, A16Z_EXAMPLES)
    
    if "error" in result:
        return f"❌ Error: {result.get('details', 'Unknown error')}", json.dumps(result, indent=2)
    
    scores = result["scores"]
    score_display = f"""
# 🚀 a16z Investment Lens

## Investment Decision
### Stage: **{result.get("investment_stage", "Unknown")}**
### Overall Score: {"🔥" * scores["overall"]} **{scores["overall"]}/5**

---

## Evaluation Scores

| Dimension | Score | What a16z Looks For |
|-----------|-------|---------------------|
| **Technical Vision** | {"⭐" * scores["technical_vision"]} {scores["technical_vision"]}/5 | Bold technical bet, "software eating X" |
| **Network Effects** | {"⭐" * scores["network_effects"]} {scores["network_effects"]}/5 | Gets stronger as it grows |
| **Contrarian Insight** | {"⭐" * scores["contrarian_insight"]} {scores["contrarian_insight"]}/5 | Non-obvious truth others miss |
| **Founder Conviction** | {"⭐" * scores["founder_conviction"]} {scores["founder_conviction"]}/5 | Compelling vision of the future |
| **Platform Potential** | {"⭐" * scores["platform_potential"]} {scores["platform_potential"]}/5 | Can become infrastructure |

---

## Most Similar a16z Company
**{result.get("most_similar_a16z_company", "N/A")}**

---

## 💪 Strengths
{chr(10).join("✅ " + s for s in result.get("strengths", []))}

## ⚠️ Concerns
{chr(10).join("🚩 " + c for c in result.get("concerns", []))}

---

## 🎯 a16z Investment Thesis
{result.get("a16z_thesis", "Not ready for institutional investment at this time.")}

---

## 🤝 Portfolio Fit & Network Value
{result.get("portfolio_fit", "Limited network synergies identified.")}

---

## 📊 Detailed Reasoning

### Technical Vision
{result["reasoning"].get("technical_vision", "N/A")}

### Network Effects
{result["reasoning"].get("network_effects", "N/A")}

### Contrarian Insight
{result["reasoning"].get("contrarian_insight", "N/A")}

### Founder Conviction
{result["reasoning"].get("founder_conviction", "N/A")}

### Platform Potential
{result["reasoning"].get("platform_potential", "N/A")}

### Overall Assessment
{result["reasoning"].get("overall", "N/A")}

---

*Evaluated against {len(A16Z_EXAMPLES)} a16z portfolio companies*
"""
    return score_display, json.dumps(result, indent=2)


# Sample pitch pre-loaded for demo
SAMPLE_PITCH = """
We're building Lumina, an AI-powered video editing platform for creators.

Problem: Video editing is still stuck in the desktop era. Creators spend 80% of their time 
on tedious tasks (cutting silences, adding captions, finding b-roll) and only 20% on creative 
work. Current tools like Premiere and Final Cut are too complex for the 50M+ content creators 
who just want to tell stories.

Solution: AI-native video editor in the browser. You upload raw footage, describe what you want, 
and our AI handles the technical work - auto-cuts silences, generates captions in 100+ languages, 
suggests b-roll from our licensed library, and even creates custom background music. Creators 
focus on storytelling, not technical skills.

Technical Moat: We've built our own video understanding models (not OpenAI wrappers). Our models 
understand context, pacing, and emotional beats. We process 4K video in real-time using custom 
WebGPU pipeline - 10x faster than competitors. All in-browser, no uploads needed.

Network Effects: Every edit improves our models. Creators share templates with their communities. 
When one gaming creator's style goes viral, 10K others copy it through our platform. We're becoming 
the Adobe of the creator economy.

Traction: $2M ARR, 50K creators (20K paid), 500K videos created. Revenue grew 4x last quarter. 
NRR 130%. Avg customer creates 12 videos/month and refers 3 friends. Top creators have 10M+ views 
on content made with Lumina.

Market: Creator economy is $100B+ and growing. 50M content creators globally, 2M posting weekly. 
Wedge is YouTube/TikTok creators, then expanding to corporate video teams and education.

Team: Both founders are ex-YouTube ML engineers who built recommendation systems. We have 15 people, 
12 engineers. Raised $3M seed from Kleiner Perkins 14 months ago. Now raising Series A.

Vision: Every smartphone will have an AI video editor. We're building the creative tools for the 
next billion storytellers.
"""

# Create Gradio interface
demo = gr.Interface(
    fn=run_evaluation,
    inputs=gr.Textbox(
        lines=20,
        placeholder="Paste your pitch transcript here...",
        label="📝 Pitch Transcript",
        value=SAMPLE_PITCH
    ),
    outputs=[
        gr.Markdown(label="🚀 a16z Evaluation"),
        gr.Code(label="Raw JSON Output", language="json")
    ],
    title="🚀 a16z Pitch Evaluator",
    description="Evaluate your startup pitch using Andreessen Horowitz's investment framework. Based on analysis of 30 a16z portfolio companies across software, crypto, bio, and consumer.",
    theme=gr.themes.Monochrome(),
    examples=[
        ["We're building a decentralized social network where users own their data and content. Unlike Twitter or Facebook, we use blockchain to ensure creators get paid directly by their audience with zero platform fees. We have 100K users and $500K in creator earnings in our first 6 months."],
        ["We're creating AI-powered drug discovery software. Our models can predict protein folding 100x faster than AlphaFold. We've already identified 3 promising cancer drug candidates. Partnered with 2 pharma companies. Team of PhD computational biologists from Stanford."],
    ]
)

if __name__ == "__main__":
    demo.launch()

# 🌲 Sequoia Pitch Evaluator

Evaluate your startup pitch using Sequoia Capital's investment framework — backed by analysis of **28 iconic portfolio companies** including Stripe, Airbnb, Zoom, Snowflake, Figma, and more.

## What It Does

Paste in your pitch transcript and get an instant structured evaluation across Sequoia's core investment dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| 🏆 **Market Leadership** | Can this be the unambiguous #1 in its category? |
| 🛡️ **Technical Moat** | Is the business defensible — technical, data, network, or regulatory barriers? |
| 💰 **Unit Economics** | Current margins and path to 70%+ gross margins with strong LTV/CAC |
| 👥 **Founder Scaling** | Can the founders hire executives and build a 1,000+ person company? |
| 🌐 **Category Creation** | New market creation or incumbent displacement? How big could the category become? |

You also get:
- **Investment stage recommendation** (Seed / Series A / Series B / Growth / Not ready)
- **Most similar Sequoia portfolio company** (and why)
- **Investment thesis** written as a Sequoia partner memo
- **Key milestones** to unlock the next funding round

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourname/sequoia-pitch-evaluator
cd sequoia-pitch-evaluator
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Launch the app

```bash
python app_sequoia.py
```

Then open your browser to `http://localhost:7860`

## File Structure

```
sequoia-pitch-evaluator/
├── app_sequoia.py              # Gradio UI — run this to launch
├── evaluator_sequoia.py        # Core evaluation logic (OpenAI API calls)
├── sequoia_examples.json       # 28 curated Sequoia portfolio companies
├── sample_pitches/
│   ├── strong_enterprise_saas.txt   # Strong pitch (scores 4-5)
│   ├── too_early_consumer.txt       # Too early (scores 1-2)
│   └── growth_stage.txt            # Growth stage (scores Series B/C)
├── requirements.txt
├── .env.example
└── README.md
```

## Portfolio Companies Used for Evaluation

The `sequoia_examples.json` covers 28 companies across stages and sectors:

**Infrastructure & Developer Tools**
Stripe, MongoDB, HashiCorp, Meraki

**Data & Analytics**
Snowflake, Cohesity

**Enterprise SaaS**
Zoom, ServiceNow, Okta, PagerDuty, Veeva Systems, Figma

**Marketplaces**
Airbnb, DoorDash, Instacart, Faire, Samsara

**Fintech**
Klarna, Plaid, Robinhood, Nubank

**Consumer & Social**
WhatsApp, YouTube, Dropbox, Notion

**Life Sciences**
Natera, Guardant Health

**Gaming & 3D**
Unity Technologies, OpenAI

## How the Scoring Works

Each dimension is scored 1–5 against Sequoia's actual bar:

- **5** — Portfolio-ready. Clear path to market leadership, comparable to top Sequoia investments
- **4** — Strong. Would generate serious interest, a few things to de-risk  
- **3** — Interesting. Real potential but needs work on key dimensions
- **2** — Concerns. Fundamental questions about the thesis that need answers
- **1** — Pass. Not ready for institutional venture investment

The evaluator uses GPT-4o with 5 portfolio companies as few-shot examples, selected for diversity across stages and sectors.

## Customization

### Add more portfolio companies
Edit `sequoia_examples.json` to add companies. Each entry follows this schema:

```json
{
  "name": "Company Name",
  "stage_at_investment": "Series A",
  "problem": "What pain they solved",
  "solution": "How they solved it",
  "traction": "Key metrics at time of Sequoia investment",
  "market": "Market size and opportunity",
  "founder_signal": "Why the founders were uniquely qualified",
  "sequoia_thesis": "Why Sequoia specifically invested — their angle"
}
```

### Adjust the scoring rubric
Edit the prompt in `evaluator_sequoia.py` → `evaluate_pitch_sequoia()` to change how dimensions are weighted or described.

### Add a new VC framework
The evaluator architecture is modular. Copy `evaluator_sequoia.py` and swap the scoring dimensions for any other VC firm's framework (a16z, Benchmark, YC, etc.).

## Limitations

- Evaluation quality depends on the detail in your pitch transcript — vague pitches get vague evaluations
- GPT-4o has a knowledge cutoff and may not know recent market developments
- This is an educational tool and does not represent official Sequoia Capital views
- Scores are indicative, not predictive of actual fundraising outcomes

## License

MIT — use freely, build on it, give feedback.

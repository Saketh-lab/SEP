# 🚀 a16z Pitch Evaluator

An AI-powered startup pitch evaluation system based on Andreessen Horowitz's investment framework. Evaluates pitches on technical vision, network effects, contrarian insights, founder conviction, and platform potential.

Built for hackathons - from idea to demo in 24 hours.

## What This Does

- Evaluates startup pitches using a16z's investment criteria
- Compares your pitch against 30 iconic a16z portfolio companies
- Provides detailed scores, investment thesis, and actionable feedback
- Suggests appropriate funding stage (Seed/Series A/B/Growth)
- Identifies portfolio fit and network synergies

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

Create a `.env` file in the project directory:

```bash
OPENAI_API_KEY=your-api-key-here
```

Or export it directly:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Run the App

```bash
python app_a16z.py
```

The Gradio interface will launch at `http://localhost:7860`

## File Structure

```
/a16z-pitch-evaluator
├── app_a16z.py              # Gradio web interface
├── evaluator_a16z.py        # Core evaluation logic
├── a16z_examples.json       # 30 a16z portfolio companies
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## How It Works

### Evaluation Criteria (a16z Framework)

1. **Technical Vision** (1-5)
   - Is this a bold technical bet?
   - Does it leverage "software eating the world"?

2. **Network Effects** (1-5)
   - Does it get stronger as it grows?
   - Are there built-in viral mechanics?

3. **Contrarian Insight** (1-5)
   - Is this a non-obvious truth others are missing?
   - Does it challenge conventional wisdom?

4. **Founder Conviction** (1-5)
   - Can they articulate a compelling vision of the future?
   - Do they have the conviction to go contrarian?

5. **Platform Potential** (1-5)
   - Can this become infrastructure others build on?
   - Is there ecosystem potential?

### Example Output

The evaluator returns:
- ⭐ Scores on each dimension (1-5 scale)
- 📊 Detailed reasoning for each score
- 🎯 Investment thesis (if fundable)
- 🤝 Portfolio fit & network synergies
- ⚠️ Key concerns and red flags
- ✅ Core strengths
- 🏢 Most similar a16z company
- 📈 Suggested investment stage

## Usage Examples

### Sample Pitch (Pre-loaded)

A sample AI video editing pitch is pre-loaded in the interface for quick demos. Just click "Submit" to see it evaluated.

### Your Own Pitch

Paste your pitch transcript into the text box. Include:
- Problem statement
- Solution overview
- Traction/metrics
- Market size
- Team background
- Technical differentiation
- Vision/future state

## Customization

### Adjust Evaluation Criteria

Edit `evaluator_a16z.py` and modify the prompt to emphasize different aspects:

```python
prompt = f"""
You are an a16z partner evaluating startup pitches.

[Add your custom evaluation criteria here]
"""
```

### Add More Portfolio Companies

Edit `a16z_examples.json` to add companies:

```json
{
  "name": "New Company",
  "stage_at_investment": "Series A",
  "problem": "...",
  "solution": "...",
  "traction": "...",
  "market": "...",
  "founder_signal": "...",
  "a16z_thesis": "..."
}
```

### Change the Model

In `evaluator_a16z.py`, update the model parameter:

```python
model="gpt-4o"  # or "gpt-4-turbo", "gpt-3.5-turbo", etc.
```

## Hackathon Tips

### Hour 0-2: Setup
- Clone this repo
- Get OpenAI API key
- Test with sample pitch

### Hour 2-8: Customize
- Add more portfolio companies relevant to your domain
- Tweak evaluation criteria for your use case
- Add example pitches for different scenarios

### Hour 8-16: Polish
- Add streaming responses (more impressive live)
- Create comparison view (multiple pitches side-by-side)
- Add export functionality (PDF reports)

### Hour 16-24: Demo Prep
- Prepare 3 test pitches (strong, weak, edge case)
- Practice your demo flow
- Deploy to Hugging Face Spaces for public URL

## Demo Script

1. **Show the interface** - "This evaluates pitches using a16z's framework"
2. **Submit sample pitch** - Click submit on pre-loaded example
3. **Highlight unique features**:
   - "Technical Vision" score (a16z specific)
   - "Portfolio Fit" section (network effects)
   - Contrarian insight evaluation
4. **Show raw JSON** - "Clean structured output for integrations"
5. **Explain data** - "Built on 30 a16z portfolio companies"

## Advanced Features (If Time Permits)

### Batch Evaluation
Process multiple pitches at once:

```python
pitches = [pitch1, pitch2, pitch3]
results = [safe_evaluate_a16z(p, A16Z_EXAMPLES) for p in pitches]
```

### Comparative Analysis
Compare two pitches side-by-side:

```python
def compare_pitches(pitch_a, pitch_b):
    result_a = safe_evaluate_a16z(pitch_a, A16Z_EXAMPLES)
    result_b = safe_evaluate_a16z(pitch_b, A16Z_EXAMPLES)
    # Generate comparison report
```

### Stage-Specific Evaluation
Filter portfolio companies by stage:

```python
seed_companies = [c for c in A16Z_EXAMPLES if c["stage_at_investment"] == "Seed"]
evaluate_pitch_a16z(pitch, seed_companies)
```

## Deployment

### Hugging Face Spaces (Free)

1. Create account at https://huggingface.co
2. Create new Space (Gradio template)
3. Upload all files
4. Add OpenAI API key in Settings → Secrets
5. Get public URL to share

### Local Network

```bash
python app_a16z.py --server-name 0.0.0.0 --server-port 7860
```

Access from other devices on your network at `http://YOUR-IP:7860`

## Troubleshooting

### "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
Make sure your `.env` file exists and contains:
```
OPENAI_API_KEY=sk-...
```

### JSON Parsing Errors
The code includes retry logic, but if you see persistent errors:
1. Lower the temperature in `evaluator_a16z.py` (already at 0.3)
2. Add more explicit JSON formatting instructions to the prompt

### Gradio Not Launching
Try specifying a different port:
```bash
python app_a16z.py --server-port 7861
```

## Credits

- Built on OpenAI's GPT-4
- UI powered by Gradio
- Portfolio data sourced from public a16z announcements and press releases

## License

MIT License - feel free to use, modify, and distribute

## Questions?

This is a hackathon project built for rapid prototyping. For production use, consider:
- Adding authentication
- Implementing rate limiting
- Caching evaluations
- Using a fine-tuned model with your own data
- Adding human-in-the-loop validation

---

**Built with ❤️ for hackathons**

Good luck with your pitch! 🚀

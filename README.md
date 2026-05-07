# Paragon RFQ Agent

A confidence-calibrated Request for Quote agent for industrial distribution. Built to demo how an LLM-powered agent handles the real-world problem: a contractor sends a vague email and the agent must decide what to infer vs. what to ask — without making a mistake that causes a return.

---

## What it does

The agent reads an incoming customer RFQ email, cross-references the customer's purchase history, and makes one of two decisions:

**AUTO-FILL** — The agent is confident enough to draft a full quote with matched SKUs, quantities, and prices. This happens when the request closely matches past orders.

**ESCALATE** — The agent surfaces clarifying questions for a human rep instead of guessing. This happens when the request is ambiguous, uses a new product type, or has quantities outside the customer's normal range.

Every response includes a **confidence score (0–100)** with an explanation of the reasoning — what signals drove the decision and what risks exist even on high-confidence fills.

### Demo samples included

| Sample | Customer | What makes it interesting |
|--------|----------|--------------------------|
| "Same as last time, usual quantities" | Hargrove Mechanical | Vague but repeat pattern — should auto-fill |
| "Maybe a size up this time" | Coastline HVAC | One ambiguous parameter breaks the match |
| "Hydraulic fittings, new to us" | Rio Grande Plumbing | New product category — no history at all |
| "Same order as July, don't change anything" | Frontier Oilfield | Exact repeat — highest confidence case |

---

## How to run

**Requirements:** Python 3.9+, an Anthropic API key.

```bash
# 1. Clone and install
git clone https://github.com/kush-rm/paragon-rfq-agent.git
cd paragon-rfq-agent
pip install streamlit anthropic

# 2. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Run the Streamlit app
streamlit run app.py
```

The app opens at `http://localhost:8501`. Pick a customer from the sidebar, load a sample RFQ, and click **Run Agent**.

**CLI smoke test (no UI):**
```bash
python agent.py 0   # sample index 0–3
```

---

## Design decisions

### Why a single Claude call instead of a multi-step pipeline

The temptation is to build a retrieval step → reasoning step → formatting step. But for this problem, a single well-structured prompt works better at this scale. The customer history fits in one prompt comfortably (5 customers, ~3 orders each). Adding pipeline steps adds failure modes and latency without improving accuracy when the context is this small. If the catalog grew to thousands of SKUs, a retrieval step would become necessary — but the current design deliberately avoids premature complexity.

### How confidence calibration actually works

Confidence is not computed with a formula — it's a judgement the LLM makes, guided by explicit rules in the system prompt. The scoring bands are:

- **85–100**: the email clearly maps to a repeat order with specific SKUs and historical quantities
- **60–84**: likely match but one parameter is uncertain (quantity not stated, size mentioned vaguely)
- **30–59**: partial match — right product category, wrong specifics, or only partial history
- **0–29**: no history match, new product type, or description is too ambiguous to act on

The system prompt gives the model those bands and explains what "uncertain" means in each case. The model then writes a `confidence_explanation` that exposes its reasoning — this is deliberately surfaced in the UI so a human rep can audit the decision, not just trust the number.

### The core tradeoff: false positives vs. false negatives

An auto-fill that ships the wrong SKU causes a return, damages trust, and costs more than asking one question. An unnecessary escalation just slows things down. So the calibration is asymmetric: the agent is tuned to be conservative. If a critical field is ambiguous (size, material type), it escalates even if everything else matches.

This is why "maybe a size up this time" drops Coastline HVAC's confidence below auto-fill threshold despite a strong order history — "maybe" is a hedge that signals the customer isn't certain, and acting on uncertainty is the exact failure mode this demo is designed to prevent.

### What this demo doesn't handle

- Multi-turn clarification: once the human answers the questions, the agent doesn't loop back to generate the quote. That would be the next step.
- Price negotiation or discounts: prices are pulled directly from the catalog.
- Authentication, logging, or audit trails: not relevant for a demo.
- SKU disambiguation across vendors: if two vendors make a nearly identical part, the agent picks based on the customer's preferred vendor list, but doesn't surface that choice explicitly. A production system should.

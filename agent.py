# agent.py
# Core RFQ agent logic. Calls Claude to reason over customer history and decide:
# - AUTO-FILL: draft a quote
# - ESCALATE: return clarifying questions

import json
import os
import anthropic
from mock_data import CUSTOMERS, PRODUCTS

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def get_customer_context(customer_id: str) -> dict:
    """Return everything we know about a customer."""
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {}
    return customer


def build_product_catalog_summary() -> str:
    """Compact catalog string for the prompt — avoids pasting 20 full dicts."""
    lines = []
    for sku, p in PRODUCTS.items():
        stock = "IN STOCK" if p["in_stock"] else "OUT OF STOCK"
        lines.append(
            f"  {sku} | {p['description']} | ${p['unit_price']:.2f}/ea | {p['vendor']} | {stock}"
        )
    return "\n".join(lines)


def build_history_summary(customer: dict) -> str:
    """Flatten order history into a readable block for the prompt."""
    lines = []
    for order in customer.get("order_history", []):
        lines.append(f"\n  Order {order['order_id']} ({order['date']}):")
        for item in order["items"]:
            lines.append(f"    - {item['sku']} × {item['qty']}  ({item['description']})  @ ${item['unit_price']:.2f}")
        if order["notes"]:
            lines.append(f"    Note: \"{order['notes']}\"")
    return "\n".join(lines) if lines else "  (no history)"


SYSTEM_PROMPT = """You are an RFQ (Request for Quote) agent for an industrial distribution company.
Your job is to read an incoming customer email, examine their purchase history, and decide whether
you can confidently auto-fill a quote or whether you need to escalate to a human rep.

You will respond ONLY with a valid JSON object — no markdown, no commentary outside the JSON.

Decision rules:
- AUTO_FILL when: the email clearly maps to items the customer has ordered before, quantities are
  reasonable (within ~2× of historical), and you can match specific SKUs with high confidence.
- ESCALATE when: the request is ambiguous about size/type, mentions a new product category,
  asks for quantities far outside history, or the description could match multiple SKUs.
- IMPORTANT: When the customer says "last time", "like before", "as usual", or "same as always",
  you MUST use ONLY the most recent order (the one with the latest date) as the basis for the quote.
  Do NOT average across orders or flag differences between older orders as ambiguity.
  Older orders are irrelevant when the customer explicitly references their last order.
  This is a firm rule: most recent order = ground truth for "last time" references.

Confidence score (0–100):
- 85–100: clear repeat order, exact or near-exact match
- 60–84: likely match but one parameter is uncertain (e.g., quantity unspecified)
- 30–59: partial match or vague category match only
- 0–29: no history match, new product type, or too ambiguous to act

Output schema:
{
  "decision": "AUTO_FILL" | "ESCALATE",
  "confidence": <int 0-100>,
  "confidence_explanation": "<2-3 sentences explaining the score>",
  "customer_name": "<name>",
  "drafted_quote": [
    {
      "sku": "<SKU>",
      "description": "<product description>",
      "qty": <int>,
      "unit_price": <float>,
      "line_total": <float>,
      "inference_note": "<why this line was chosen>"
    }
  ],
  "quote_total": <float | null>,
  "clarifying_questions": ["<question>"],
  "reasoning_summary": "<paragraph: what signals you used, what risks you see>"
}

Rules:
- drafted_quote is populated for AUTO_FILL; clarifying_questions is empty or minimal.
- clarifying_questions is populated for ESCALATE; drafted_quote may be empty or a best-guess
  partial that you flag explicitly.
- Always fill reasoning_summary regardless of decision.
- Do not invent SKUs. Only use SKUs from the provided catalog.
- If a product is OUT OF STOCK, note it in inference_note and flag it in clarifying_questions
  even on AUTO_FILL decisions.
"""


def run_rfq_agent(customer_id: str, email_text: str) -> dict:
    """
    Main entry point. Returns parsed JSON dict from Claude.
    Raises on API error or JSON parse failure.
    """
    customer = get_customer_context(customer_id)
    if not customer:
        raise ValueError(f"Unknown customer ID: {customer_id}")

    history_block = build_history_summary(customer)
    catalog_block = build_product_catalog_summary()

    user_message = f"""CUSTOMER PROFILE
Name: {customer['name']}
Contact: {customer['contact']}
Preferred vendors: {', '.join(customer['preferred_vendors'])}
Payment terms: {customer['payment_terms']}

ORDER HISTORY
{history_block}

PRODUCT CATALOG
{catalog_block}

INCOMING RFQ EMAIL
---
{email_text.strip()}
---

Analyze this RFQ and return the JSON response per your instructions."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if Claude adds them despite instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)


if __name__ == "__main__":
    # Quick CLI smoke test
    import sys
    from mock_data import SAMPLE_RFQS

    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    sample = SAMPLE_RFQS[idx]
    print(f"\n=== Sample: {sample['label']} ===\n")
    print(f"Customer: {sample['customer_id']}")
    print(f"\nEmail:\n{sample['email']}\n")

    result = run_rfq_agent(sample["customer_id"], sample["email"])
    print(json.dumps(result, indent=2))

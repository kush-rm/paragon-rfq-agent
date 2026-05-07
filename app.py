# app.py
# Streamlit UI for the RFQ confidence calibration agent.

import streamlit as st
from mock_data import CUSTOMERS, SAMPLE_RFQS
from agent import run_rfq_agent

st.set_page_config(
    page_title="Paragon RFQ Agent",
    page_icon="🔩",
    layout="wide",
)

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.confidence-bar-wrap { background: #e5e7eb; border-radius: 8px; height: 18px; width: 100%; margin-bottom: 8px; }
.confidence-bar { height: 18px; border-radius: 8px; transition: width 0.4s ease; }
.badge-auto  { background:#16a34a; color:#fff; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.9rem; }
.badge-escalate { background:#dc2626; color:#fff; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.9rem; }
.info-box { background:#f0f9ff; border-left:4px solid #0ea5e9; padding:12px 16px; border-radius:4px; margin:8px 0; }
.warn-box { background:#fff7ed; border-left:4px solid #f97316; padding:12px 16px; border-radius:4px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🔩 Paragon RFQ Agent")
st.caption("Confidence-calibrated quoting for industrial distribution — demo with mock data")
st.divider()

# ── Sidebar: customer + sample loader ────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")

    customer_options = {cid: f"{cid} — {c['name']}" for cid, c in CUSTOMERS.items()}
    selected_customer_id = st.selectbox(
        "Customer",
        options=list(customer_options.keys()),
        format_func=lambda k: customer_options[k],
    )
    customer = CUSTOMERS[selected_customer_id]

    st.markdown(f"**Contact:** {customer['contact']}")
    st.markdown(f"**Preferred vendors:** {', '.join(customer['preferred_vendors'])}")
    st.markdown(f"**Payment terms:** {customer['payment_terms']}")
    st.markdown(f"**Past orders:** {len(customer['order_history'])}")

    st.divider()
    st.subheader("Load a sample RFQ")
    for i, sample in enumerate(SAMPLE_RFQS):
        if st.button(sample["label"], key=f"sample_{i}"):
            st.session_state["rfq_email"] = sample["email"]
            st.session_state["sample_customer"] = sample["customer_id"]
            # Switch the selectbox by re-running — we store the override
            st.session_state["override_customer"] = sample["customer_id"]
            st.rerun()

# Honor customer override from sample loader
if "override_customer" in st.session_state:
    override = st.session_state.pop("override_customer")
    # We can't retroactively change the selectbox value in Streamlit without rerun,
    # but we can use the override for the actual API call below.
    selected_customer_id = override

# ── Main input ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Incoming RFQ Email")
    email_text = st.text_area(
        "Paste the customer email here",
        value=st.session_state.get("rfq_email", ""),
        height=220,
        placeholder="e.g. Hey, need to reorder the brass fittings like last time...",
        key="rfq_email_input",
    )

    run_btn = st.button("Run Agent", type="primary", use_container_width=True)

# ── Order history preview ────────────────────────────────────────────────────
with col_right:
    st.subheader(f"History — {customer['name']}")
    for order in customer["order_history"]:
        with st.expander(f"Order {order['order_id']}  ({order['date']})  — ${order['total']:,.2f}"):
            for item in order["items"]:
                st.markdown(f"- **{item['sku']}** × {item['qty']}  |  {item['description']}  |  ${item['unit_price']:.2f}/ea")
            if order["notes"]:
                st.markdown(f"*Note: \"{order['notes']}\"*")

st.divider()

# ── Agent output ─────────────────────────────────────────────────────────────
if run_btn:
    email_value = st.session_state.get("rfq_email_input") or email_text
    if not email_value.strip():
        st.warning("Please paste an RFQ email before running the agent.")
        st.stop()

    with st.spinner("Agent is analyzing the RFQ..."):
        try:
            result = run_rfq_agent(selected_customer_id, email_value)
        except Exception as e:
            st.error(f"Agent error: {e}")
            st.stop()

    decision = result.get("decision", "ESCALATE")
    confidence = result.get("confidence", 0)

    # Confidence bar color
    if confidence >= 85:
        bar_color = "#16a34a"
    elif confidence >= 60:
        bar_color = "#ca8a04"
    else:
        bar_color = "#dc2626"

    badge_html = (
        '<span class="badge-auto">AUTO-FILL</span>'
        if decision == "AUTO_FILL"
        else '<span class="badge-escalate">ESCALATE TO HUMAN</span>'
    )

    # ── Decision header ───────────────────────────────────────────────────────
    st.subheader("Agent Decision")
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown(f"**Outcome:** {badge_html}", unsafe_allow_html=True)
        st.markdown(
            f"""<div class="confidence-bar-wrap">
                  <div class="confidence-bar" style="width:{confidence}%;background:{bar_color};"></div>
               </div>""",
            unsafe_allow_html=True,
        )
        st.markdown(f"**Confidence: {confidence}/100** — {result.get('confidence_explanation', '')}")
    with hcol2:
        st.metric("Score", f"{confidence}", delta=None)

    st.markdown(
        f'<div class="info-box">{result.get("reasoning_summary", "")}</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    res_col1, res_col2 = st.columns(2)

    # ── Drafted quote ─────────────────────────────────────────────────────────
    with res_col1:
        st.subheader("Drafted Quote")
        quote_lines = result.get("drafted_quote", [])
        if quote_lines:
            for line in quote_lines:
                stock_warn = ""
                if "out of stock" in line.get("inference_note", "").lower():
                    stock_warn = " ⚠️ OUT OF STOCK"
                st.markdown(
                    f"**{line['sku']}** — {line['description']}{stock_warn}  \n"
                    f"Qty: `{line['qty']}` × ${line['unit_price']:.2f} = **${line['line_total']:.2f}**  \n"
                    f"*{line.get('inference_note', '')}*"
                )
                st.markdown("---")
            total = result.get("quote_total")
            if total:
                st.markdown(f"### Total: ${total:,.2f}")
        else:
            st.markdown("*No quote drafted — agent is escalating.*")

    # ── Clarifying questions ──────────────────────────────────────────────────
    with res_col2:
        st.subheader("Clarifying Questions")
        questions = result.get("clarifying_questions", [])
        if questions:
            for q in questions:
                st.markdown(
                    f'<div class="warn-box">❓ {q}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("*No questions — agent is confident enough to auto-fill.*")

    # ── Raw JSON expander ─────────────────────────────────────────────────────
    with st.expander("Raw agent response (JSON)"):
        st.json(result)

import streamlit as st
import pandas as pd
import sqlite3
from agent_engine import process_recovery
from database import log_audit, init_db

init_db()

st.set_page_config(page_title="Autonomous Recovery Agent", layout="wide")
st.title("🛡️ Razorpay Autonomous Settlement & Recovery Agent")
st.caption("Track 01: AI Growth & Agentic Commerce | Explainable, Bounded & Gated Execution")

st.sidebar.header("Simulate Failed Transaction")
sim_order_id = st.sidebar.text_input("Order ID", "order_test_101")
sim_amount = st.sidebar.number_input("Cart Amount (₹)", min_value=100.0, value=1200.0, step=50.0)
sim_error = st.sidebar.selectbox("Failure Reason", [
    "PAYMENT_TIMED_OUT_NETWORK_ERROR",
    "CARD_DECLINED_INSUFFICIENT_FUNDS",
    "USER_DROPPED_AT_OTP"
])
sim_attempts = st.sidebar.slider("Prior Retries", 0, 4, 1)

if st.sidebar.button("Simulate & Run Agent"):
    with st.spinner("Agent evaluating recovery policy..."):
        res = process_recovery(sim_order_id, sim_amount, sim_error, sim_attempts)
        log_audit(
            res["order_id"], res["original_amount"], res["failure_reason"],
            res["ai_reasoning"], res["approved_discount_pct"], res["final_amount"],
            res["payment_link"], res["status"]
        )
        st.sidebar.success("Action logged & processed!")

st.subheader("Live Explainable Audit Trail")
conn = sqlite3.connect("audit_trail.db")
df = pd.read_sql_query("SELECT * FROM recovery_audit ORDER BY id DESC", conn)
conn.close()

if not df.empty:
    st.dataframe(df, width=1200)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events Analyzed", len(df))
    col2.metric("Successful Links Dispatched", len(df[df["status"] == "SUCCESS_LINK_GENERATED"]))
    col3.metric("Spam/Risk Blocked", len(df[df["status"] == "REJECTED"]))
else:
    st.info("No audit events recorded yet. Run a simulation from the sidebar.")
# 🛡️ Autonomous Settlement & Recovery Agent for Agentic Commerce

> Built for the **Razorpay Buildathon — Track 01: AI Growth & Agentic Commerce**

An autonomous, bounded agent system that detects failed checkout transactions, evaluates failure root causes (network timeouts, friction, bank declines), dynamically applies rule-governed recovery incentives, and dispatches automated Razorpay payment links with a complete explainable audit trail.

---

## 🎯 Key Capabilities & Architecture

- **Context-Aware Recovery Logic:** Differentiates between drop-offs, gateway timeouts, and bank declines to choose the optimal recovery path.
- **Strict Deterministic Guardrails (Bounded & Gated):**
  - Maximum discount strictly capped at 10%.
  - Order floor requirement (₹500 min) to protect merchant margins.
  - Maximum retry ceilings (blocked after 3 retries to prevent customer spam).
- **End-to-End Audit Trail:** Persists all agent decisions, policy evaluations, and payment API events to SQLite for complete financial explainability.
- **Interactive Merchant Dashboard:** Built with Streamlit for real-time transaction simulation, metric monitoring, and audit log analysis.

---

## 🛠️ Tech Stack

- **Backend & Logic:** Python 3.12, FastAPI
- **Payment Gateway:** Razorpay Python SDK (Test Mode APIs)
- **Data & State Persistence:** SQLite, Pandas
- **Frontend / UI:** Streamlit
- **Environment Management:** python-dotenv

---

## 🚀 Getting Started

### 1. Clone & Set Up Environment
```bash
git clone <your-repo-url>
cd razorpay-recovery-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
import streamlit as st
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Inline simulated data — no backend import needed
import random

SCENARIOS = [
    {"cpu": "92%", "memory": "78%", "error_rate": "34%"},
    {"cpu": "45%", "memory": "91%", "error_rate": "5%"},
    {"cpu": "21%", "memory": "30%", "error_rate": "67%"},
    {"cpu": "88%", "memory": "85%", "error_rate": "22%"},
    {"cpu": "12%", "memory": "15%", "error_rate": "2%"},
]

SAMPLE_LOGS = [
    "ERROR: Connection timeout after 30s. Service: payment-api. Pod: payment-7f9d-xkz2p",
    "CRITICAL: Out of memory. Killed process: auth-service. Node: node-02",
    "ERROR: 503 Service Unavailable. Upstream: order-service. Retries: 5",
    "WARN: CPU throttling detected. Container: recommendation-engine. Limit: 500m",
    "ERROR: Database connection pool exhausted. Service: user-api. Pool size: 10",
]

st.set_page_config(
    page_title="AI DevOps Copilot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI DevOps Copilot")
st.caption("Agentic log analysis · Root cause detection · Self-healing simulation")
st.divider()

if "metrics" not in st.session_state:
    st.session_state.metrics = random.choice(SCENARIOS)
if "sample_log" not in st.session_state:
    st.session_state.sample_log = random.choice(SAMPLE_LOGS)

metrics = st.session_state.metrics

st.subheader("📊 System metrics (simulated)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU usage",    metrics["cpu"])
col2.metric("Memory usage", metrics["memory"])
col3.metric("Error rate",   metrics["error_rate"])
col4.metric(
    "Status",
    "🔴 Degraded" if int(metrics["cpu"].replace("%", "")) > 80 else "🟢 Healthy"
)

st.divider()
st.subheader("🔍 Analyze logs")

log_input = st.text_area(
    "Paste a log entry",
    value=st.session_state.sample_log,
    height=100,
)

col_a, col_b, col_c = st.columns(3)
cpu_input = col_a.text_input("CPU",        value=metrics["cpu"])
mem_input = col_b.text_input("Memory",     value=metrics["memory"])
err_input = col_c.text_input("Error rate", value=metrics["error_rate"])

col_btn1, col_btn2 = st.columns([1, 5])
run = col_btn1.button("🚀 Run analysis", type="primary")
if col_btn2.button("🔄 New sample"):
    st.session_state.metrics    = random.choice(SCENARIOS)
    st.session_state.sample_log = random.choice(SAMPLE_LOGS)
    st.rerun()

if run:
    if not log_input.strip():
        st.warning("Please enter a log entry.")
    else:
        with st.spinner("Running agentic pipeline... Agent 1 → Agent 2 → Agent 3"):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/analyze",
                    json={
                        "log": log_input,
                        "metrics": {
                            "cpu":        cpu_input,
                            "memory":     mem_input,
                            "error_rate": err_input,
                        },
                    },
                    timeout=60,
                )
                result = response.json()

                st.divider()
                st.subheader("📋 Analysis result")

                resolved = result.get("auto_resolved", False)
                severity = result.get("severity_tag", "Unknown")

                banner_col1, banner_col2 = st.columns(2)
                banner_col1.info(f"**Severity:** {severity}")
                if resolved:
                    banner_col2.success("✅ Auto-resolved by self-healing simulation")
                else:
                    banner_col2.warning("⚠️ Requires manual intervention — alert sent")

                st.divider()
                st.error(f"**🔴 Error type:** {result['error_type']}")
                st.info(f"**🔵 Root cause:** {result['root_cause']}")
                st.success(f"**🟢 Suggested fix:** {result['suggested_fix']}")
                st.warning(f"**🟡 Action taken:** {result['action_taken']}")
                st.caption(f"Confidence: {result['confidence']}")

                st.divider()
                st.subheader("🔄 Agent pipeline trace")
                st.markdown("""
| Step | Agent | Action |
|------|-------|--------|
| 1 | 🧠 Analyzer Agent | Parsed log + metrics, ran LLM root cause analysis |
| 2 | 🎯 Decision Agent | LLM selected remediation action label |
| 3 | ⚡ Action Agent | Decision Engine applied rules + ran simulation |
""")

                with st.expander("📦 Raw JSON response"):
                    st.json(result)

            except httpx.ConnectError:
                st.error("❌ Cannot connect to backend. Check your BACKEND_URL in .env")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
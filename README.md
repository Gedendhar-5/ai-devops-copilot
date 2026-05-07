Readme · MD
Copy

# 🤖 AI DevOps Copilot with Agentic Self-Healing & Observability Intelligence
 
> An intelligent, agent-driven system that monitors application logs and system metrics, detects anomalies, performs root cause analysis using LLMs, and autonomously simulates self-healing infrastructure actions.
 
---
 
## 📸 Screenshots
 
### Dashboard — System Metrics
<!-- PASTE SCREENSHOT HERE: Streamlit dashboard showing CPU, Memory, Error Rate metric cards -->
 
---
 
### Log Analysis — Input
<!-- PASTE SCREENSHOT HERE: Streamlit dashboard showing log input box and metric fields -->
 
---
 
### Analysis Result — Output
<!-- PASTE SCREENSHOT HERE: Streamlit showing Error Type, Root Cause, Suggested Fix, Action Taken cards -->
 
---
 
### Agent Pipeline Trace
<!-- PASTE SCREENSHOT HERE: Streamlit showing the 3-agent pipeline trace table -->
 
---
 
### FastAPI Swagger UI
<!-- PASTE SCREENSHOT HERE: http://localhost:8000/docs showing GET /health and POST /analyze -->
 
---
 
### GitHub Actions CI Pipeline
<!-- PASTE SCREENSHOT HERE: GitHub Actions tab showing green CI runs -->
 
---
 
### Render Deployment
<!-- PASTE SCREENSHOT HERE: Render dashboard showing deployed backend service -->
 
---
 
### Streamlit Cloud Deployment
<!-- PASTE SCREENSHOT HERE: Streamlit Cloud showing deployed frontend app -->
 
---
 
## 🧠 Project Overview
 
The AI DevOps Copilot is a production-grade, portfolio-level system that combines **Generative AI**, **Agentic workflows**, and **DevOps engineering** to create a system that not only understands infrastructure issues but makes decisions like a senior DevOps engineer.
 
It ingests raw application logs and simulated system metrics, runs them through a multi-agent LangGraph pipeline, uses a Groq-hosted LLM for root cause analysis, applies rule-based decision logic, and simulates self-healing actions — all exposed via a FastAPI backend and Streamlit frontend dashboard.
 
---
 
## 🎯 Objectives
 
- Automate log and metric analysis end to end
- Detect anomalies and classify severity proactively
- Perform AI-driven root cause analysis using LLMs
- Enable agent-based autonomous decision making
- Simulate self-healing infrastructure actions (restart / scale / alert)
- Build a modular, production-like, deployable DevOps system
---
 
## ⚙️ Tech Stack
 
| Layer | Technology |
|-------|-----------|
| **LLM** | Groq API — llama-3.3-70b-versatile |
| **Agent Orchestration** | LangGraph — StateGraph pipeline |
| **LLM Framework** | LangChain |
| **Backend** | FastAPI + Uvicorn |
| **Data Processing** | Python Regex + Pandas |
| **Frontend** | Streamlit |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |
| **Backend Deployment** | Render (free tier) |
| **Frontend Deployment** | Streamlit Cloud (free tier) |
| **Language** | Python 3.11 |
 
---
 
## 🏗️ High-Level System Architecture
 
```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
│              Logs + Metrics (API / Streamlit UI)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PREPROCESSING LAYER                          │
│         Regex log parsing · Pandas normalization                │
│         Severity classification · Keyword extraction            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AGENTIC AI LAYER (LangGraph)                   │
│                                                                 │
│   ┌─────────────────┐   ┌──────────────────┐   ┌────────────┐   │
│   │  Analyzer Agent │ → │  Decision Agent  │ → │Action Agent│   │
│   │  Reads logs +   │   │  Picks action    │   │  Runs      │   │
│   │  metrics, calls │   │  label via LLM   │   │  simulation│   │
│   │  LLM for RCA    │   │                  │   │  + rules   │   │
│   └─────────────────┘   └──────────────────┘   └────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LLM LAYER (Groq)                           │
│              llama-3.3-70b-versatile                            │
│         Root cause analysis · Decision prompting                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION ENGINE                              │
│         Rule-based overrides on top of LLM decisions            │
│         Maps issue patterns → restart / scale / alert           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SELF-HEALING SIMULATION                        │
│      Restart service · Scale replicas · Send PagerDuty alert    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                               │
│          FastAPI JSON response · Streamlit Dashboard            │
└─────────────────────────────────────────────────────────────────┘
```
 
---
 
## 🔧 Backend Architecture
 
```
backend/
├── main.py                  ← FastAPI app — POST /analyze endpoint
├── agents/
│   └── graph.py             ← LangGraph StateGraph — 3-agent pipeline
├── core/
│   ├── preprocessor.py      ← Regex log parser + Pandas normalizer
│   ├── llm.py               ← Groq API client + prompt runner
│   ├── decision_engine.py   ← Rule-based action mapper
│   └── prompts.py           ← LLM prompt templates
└── utils/
    └── metrics.py           ← Simulated metrics generator
```
 
### Request Flow (Backend)
 
```
POST /analyze
      │
      ▼
preprocessor.normalize()
  - parse_log()         → regex extracts level, service, pod, keywords
  - _extract_percent()  → "92%" → 92.0
  - _compute_severity() → critical / high / medium / low
      │
      ▼
agents/graph.run_graph()
  - analyzer_agent()    → calls llm.run_analysis()  → structured RCA
  - decision_agent()    → calls llm.run_decision()  → action label
  - action_agent()      → calls decision_engine.execute() → simulation
      │
      ▼
AnalyzeResponse
  - error_type, root_cause, suggested_fix
  - action_taken, confidence, severity_tag, auto_resolved
```
 
---
 
## 🧠 LLM Architecture
 
```
Groq API (llama-3.3-70b-versatile)
         │
         ├── Analysis Prompt  (called by Analyzer Agent)
         │     Input:  raw log, parsed fields, CPU%, memory%, error_rate%, severity
         │     Output: ERROR_TYPE / ROOT_CAUSE / SUGGESTED_FIX / CONFIDENCE
         │     Format: strict key-value for deterministic parsing
         │
         └── Decision Prompt  (called by Decision Agent)
               Input:  error_type + root_cause
               Output: one word — restart / scale / alert
               Format: single token for rule-engine compatibility
```
 
### Prompt Design Principles
 
- Temperature set to `0.2` for consistent, low-variance outputs
- Strict output format enforced (`KEY: value`) so regex can parse reliably
- Fallback parsing gracefully handles LLM format deviations
- Decision prompt constrained to 3 possible tokens to prevent hallucination
---
 
## 🤖 Agent Architecture (LangGraph)
 
```
AgentState (shared TypedDict)
    normalized → error_type → root_cause → suggested_fix
    → confidence → action_label → action_taken → severity_tag → auto_resolved
 
StateGraph flow:
 
  [START]
     │
     ▼
analyzer_agent
  - Receives: normalized (NormalizedInput)
  - Calls:    llm.run_analysis()
  - Sets:     error_type, root_cause, suggested_fix, confidence
     │
     ▼
decision_agent
  - Receives: error_type, root_cause
  - Calls:    llm.run_decision()
  - Sets:     action_label (restart / scale / alert)
     │
     ▼
action_agent
  - Receives: action_label + full normalized metrics
  - Calls:    decision_engine.execute() — applies rule overrides
  - Sets:     action_taken, severity_tag, auto_resolved
     │
     ▼
  [END]
```
 
### Decision Engine Rules (Priority Order)
 
| Rule | Condition | Action |
|------|-----------|--------|
| critical_cpu_scale | CPU ≥ 90% AND timeout keyword | scale |
| oom_restart | Memory ≥ 90% OR crash/memory keyword | restart |
| high_error_rate_alert | Error rate ≥ 50% | alert |
| db_issue_alert | database keyword detected | alert |
| high_cpu_scale | CPU ≥ 75% | scale |
| llm_fallback | No rule matched | LLM decision |
 
---
 
## 🔄 End-to-End Workflow
 
```
1. User pastes a log entry + metric values into Streamlit UI
         │
2. Streamlit sends POST /analyze to FastAPI backend
         │
3. FastAPI calls preprocessor.normalize()
   → Regex extracts: level, service, pod, keywords
   → Metrics converted: "92%" → 92.0
   → Severity computed: critical / high / medium / low
         │
4. FastAPI calls agents/graph.run_graph(normalized)
         │
5. Analyzer Agent fires
   → Builds analysis prompt with log + metrics
   → Sends to Groq LLM (llama-3.3-70b-versatile)
   → Parses structured response: error_type, root_cause, fix, confidence
         │
6. Decision Agent fires
   → Builds decision prompt with error_type + root_cause
   → Sends to Groq LLM
   → Parses action label: restart / scale / alert
         │
7. Action Agent fires
   → Passes LLM action + metrics to Decision Engine
   → Rules evaluated in priority order
   → Rule may override LLM decision
   → Simulation executed: "Simulated: System scaled — replicas increased from 2 to 4"
         │
8. FastAPI returns AnalyzeResponse JSON
         │
9. Streamlit renders:
   → Severity banner + auto-resolved status
   → Error type, root cause, suggested fix, action taken cards
   → Agent pipeline trace table
   → Raw JSON expander
```
 
---
 
## 🐳 Docker Architecture
 
```
docker-compose.yml
│
├── backend service
│     Image built from: Dockerfile
│     Base: python:3.11-slim
│     Copies: backend/ + requirements.txt
│     Runs: uvicorn backend.main:app --host 0.0.0.0 --port 8000
│     Env: GROQ_API_KEY from .env
│     Port: 8000:8000
│
└── frontend service
      Image: python:3.11-slim
      Installs: streamlit httpx python-dotenv
      Runs: streamlit run frontend/app.py --server.port 8501
      Env: BACKEND_URL=http://backend:8000
      Port: 8501:8501
      Depends on: backend
```
 
### Run with Docker
 
```bash
docker-compose up --build
```
 
Access at:
- Backend:  `http://localhost:8000/docs`
- Frontend: `http://localhost:8501`
---
 
## 🔁 CI/CD Pipeline (GitHub Actions)
 
```
.github/workflows/ci.yml
 
Trigger: push or pull_request to main branch
 
Jobs:
  test (ubuntu-latest)
    │
    ├── Step 1: Checkout code          (actions/checkout@v4)
    ├── Step 2: Set up Python 3.11     (actions/setup-python@v5)
    ├── Step 3: pip install -r requirements.txt
    ├── Step 4: Validate preprocessor  → from backend.core.preprocessor import normalize
    ├── Step 5: Validate decision engine → from backend.core.decision_engine import execute
    └── Step 6: Validate FastAPI app   → from backend.main import app
 
Purpose:
  - Validates all imports work on every push to main
  - Catches broken dependencies before Render deploys
  - Acts as a smoke test for the full module chain
  - Runs in ~45 seconds
```
 
---
 
## ☁️ Deployment Architecture
 
```
Developer (VS Code, Windows)
         │
         │ uploads via GitHub browser
         ▼
GitHub Repository (main branch)
         │
         ├─────────────────────────────────┐
         │                                 │
         ▼                                 ▼
Render (Backend)                 Streamlit Cloud (Frontend)
Detects push to main             Detects push to main
Builds Docker image              Reads frontend/app.py
Runs FastAPI on port 8000        Installs requirements.txt
Exposes public HTTPS URL         Exposes public HTTPS URL
         │                                 │
         │         API calls               │
         └─────────────────────────────────┘
 
Production URLs:
  Backend:  https://ai-devops-copilot-backend.onrender.com
  Frontend: https://your-username-ai-devops-copilot.streamlit.app
```
 
### Free Tier Summary
 
| Service | Free Tier Behaviour |
|---------|-------------------|
| Render | Sleeps after 15 min inactivity, wakes in ~30s on next request |
| Streamlit Cloud | Always on, no sleep |
| Groq API | 14,400 requests/day on llama-3.3-70b-versatile |
 
---
 
## 📁 Project Structure
 
```
ai-devops-copilot/
├── backend/
│   ├── main.py                  ← FastAPI entry point + /analyze endpoint
│   ├── agents/
│   │   ├── __init__.py
│   │   └── graph.py             ← LangGraph 3-agent StateGraph pipeline
│   ├── core/
│   │   ├── __init__.py
│   │   ├── preprocessor.py      ← Regex log parser + Pandas normalizer
│   │   ├── llm.py               ← Groq API client wrapper
│   │   ├── decision_engine.py   ← Rule-based action mapper
│   │   └── prompts.py           ← LLM prompt templates
│   └── utils/
│       ├── __init__.py
│       └── metrics.py           ← Simulated metrics + sample logs
├── frontend/
│   └── app.py                   ← Streamlit dashboard
├── .github/
│   └── workflows/
│       └── ci.yml               ← GitHub Actions CI pipeline
├── .env                         ← Secrets (never commit)
├── .env.example                 ← Safe template
├── Dockerfile                   ← Backend container definition
├── docker-compose.yml           ← Multi-service orchestration
├── requirements.txt             ← Python dependencies
└── README.md
```
 
---
 
## 🚀 Setup & Installation
 
### Prerequisites
 
- Python 3.11
- VS Code
- Groq API key — free at `console.groq.com`
### 1. Clone the Repository
 
```bash
git clone https://github.com/your-username/ai-devops-copilot.git
cd ai-devops-copilot
```
 
### 2. Create Virtual Environment
 
```bash
python -m venv .venv
 
# Windows
.venv\Scripts\activate
 
# Mac/Linux
source .venv/bin/activate
```
 
### 3. Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Configure Environment
 
```bash
cp .env.example .env
```
 
Edit `.env` and add:
 
```env
GROQ_API_KEY=gsk_your_key_here
BACKEND_URL=http://localhost:8000
```
 
### 5. Run Backend
 
```bash
uvicorn backend.main:app --reload --port 8000
```
 
Visit `http://localhost:8000/docs` for Swagger UI.
 
### 6. Run Frontend
 
Open a second terminal, activate the venv, then:
 
```bash
streamlit run frontend/app.py
```
 
Visit `http://localhost:8501` for the dashboard.
 
---
 
## 📌 API Reference
 
### POST /analyze
 
**Request:**
 
```json
{
  "log": "ERROR: Connection timeout after 30s. Service: payment-api. Pod: payment-7f9d-xkz2p",
  "metrics": {
    "cpu": "92%",
    "memory": "78%",
    "error_rate": "34%"
  }
}
```
 
**Response:**
 
```json
{
  "error_type": "Connection Timeout",
  "root_cause": "High CPU usage (92%) caused request queuing and eventual timeout in payment-api",
  "suggested_fix": "Scale payment-api horizontally and check DB connection pool limits",
  "action_taken": "Simulated: System scaled — replicas increased from 2 to 4",
  "confidence": "High",
  "severity_tag": "🔴 CRITICAL",
  "auto_resolved": true
}
```
 
### GET /health
 
```json
{ "status": "ok", "version": "1.0.0" }
```
 
---
 
## 🧪 Sample Test Inputs
 
### Connection Timeout (High CPU)
 
```json
{
  "log": "ERROR: Connection timeout after 30s. Service: payment-api. Pod: payment-7f9d-xkz2p",
  "metrics": { "cpu": "92%", "memory": "78%", "error_rate": "34%" }
}
```
 
### OOM Crash (High Memory)
 
```json
{
  "log": "CRITICAL: Out of memory. Killed process: auth-service. Node: node-02",
  "metrics": { "cpu": "45%", "memory": "95%", "error_rate": "5%" }
}
```
 
### Service Unavailable
 
```json
{
  "log": "ERROR: 503 Service Unavailable. Upstream: order-service. Retries: 5",
  "metrics": { "cpu": "88%", "memory": "85%", "error_rate": "22%" }
}
```
 
### Database Pool Exhausted
 
```json
{
  "log": "ERROR: Database connection pool exhausted. Service: user-api. Pool size: 10",
  "metrics": { "cpu": "21%", "memory": "30%", "error_rate": "67%" }
}
```
 
---
 
## 📈 Key Features
 
- **AI-powered root cause analysis** — LLM reasons about logs and metrics together
- **3-agent LangGraph pipeline** — Analyzer → Decision → Action, fully wired with shared state
- **Rule-based Decision Engine** — hard metric thresholds override LLM decisions for reliability
- **Self-healing simulation** — restart, scale, and alert actions with descriptive output
- **Severity classification** — critical / high / medium / low derived from metric thresholds
- **Modular architecture** — each layer is independently testable and replaceable
- **Full CI/CD pipeline** — GitHub Actions validates every push automatically
- **Free-tier deployment** — Render + Streamlit Cloud, zero infrastructure cost
---
 
## ⚠️ Limitations
 
- Self-healing actions are simulated — no real Kubernetes or cloud API calls
- LLM accuracy depends on Groq availability and prompt quality
- Render free tier sleeps after 15 minutes of inactivity
- No real-time log streaming — inputs are submitted manually
---
 
## 🔮 Future Enhancements
 
- Real Kubernetes integration via `kubectl` API for actual pod restarts and scaling
- Real-time log streaming using Kafka or WebSockets
- Slack and Email alert integration via webhooks
- Prometheus + Grafana for live metric ingestion
- Vector database (Pinecone / ChromaDB) for historical incident learning
- Multi-agent orchestration with parallel agent execution
- Feedback loop — user ratings improve future LLM prompts
---
 
## 🏆 Resume Highlight
 
> Developed an AI-powered DevOps Copilot with agentic workflows using LangGraph that analyzes application logs and system metrics, performs LLM-driven root cause analysis via Groq, and simulates self-healing infrastructure actions through a rule-based decision engine — deployed end-to-end on Render and Streamlit Cloud with GitHub Actions CI/CD.
 
---
 
## 🎯 Interview One-Liner
 
> "It's an AI system that monitors logs and metrics, understands incidents like a senior DevOps engineer, and autonomously decides and simulates the right fix using a 3-agent LangGraph pipeline and Groq LLM."
 
---
 
## 🤝 Contributing
 
Contributions are welcome. Open an issue or submit a pull request.
 
---
 
## 📄 License
 
This project is licensed under the MIT License.

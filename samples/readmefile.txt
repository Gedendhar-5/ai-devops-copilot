# 🚀 AI DevOps Copilot with Agentic Self-Healing & Observability Intelligence

## 🧠 Overview
AI DevOps Copilot is an intelligent, agent-driven system that monitors application logs and system metrics, detects anomalies, performs root cause analysis using Large Language Models (LLMs), and autonomously suggests or simulates remediation actions.

The system combines **LLMs, observability concepts, and agentic workflows** to reduce debugging time, improve reliability, and simulate self-healing infrastructure.

---

## 🎯 Objectives
- Automate log and metric analysis  
- Detect anomalies proactively  
- Perform AI-driven root cause analysis  
- Enable agent-based decision making  
- Simulate self-healing infrastructure  
- Build a production-like DevOps system  

---

## ⚙️ Tech Stack

### 🧠 AI / GenAI
- LLM (Groq / Llama / OpenAI)  
- Prompt Engineering  
- LangChain  
- LangGraph (Agent workflows)  

### ⚙️ Backend
- Python  
- FastAPI  

### 🔍 Data Processing
- Regex (log parsing)  
- Pandas  

### 📊 Observability
- Simulated Metrics (CPU, Memory, Error Rates)  
- (Optional) Prometheus & Grafana  

### 📊 Frontend
- Streamlit  

### 🐳 DevOps
- Docker  
- GitHub Actions (CI/CD)  

### ☁️ Deployment (Free Tier)
- Render (Backend)  
- Streamlit Cloud (Frontend)  

---

## 🏗️ System Architecture


Logs + Metrics
↓
Preprocessing (Regex, Cleaning)
↓
Observability Analysis
↓
Agentic AI Layer (LangGraph)

Analyzer Agent
Decision Agent
Action Agent
↓
LLM Processing
↓
Decision Engine
↓
Self-Healing Simulation
↓
Output (API + Dashboard)

---

## 🔄 Workflow

1. **Input Layer**
   - Logs and metrics are ingested via API or UI  

2. **Preprocessing**
   - Clean logs and extract patterns using regex  

3. **Observability Layer**
   - Analyze system metrics like CPU, memory, and error rates  

4. **Agentic AI Layer**
   - Analyzer Agent → Understand issue  
   - Decision Agent → Decide action  
   - Action Agent → Execute/simulate fix  

5. **LLM Processing**
   - Generate root cause and fix suggestions  

6. **Decision Engine**
   - Map issues to remediation actions  

7. **Self-Healing Simulation**
   - Restart services  
   - Scale systems  
   - Send alerts  

8. **Output**
   - Structured response displayed via API and dashboard  

---

## 💻 Sample Self-Healing Simulation

```python
def restart_service():
    return "Service restarted successfully (simulated)"

def scale_system():
    return "System scaled (simulated)"

def send_alert():
    return "Alert sent to DevOps team"
🚀 Getting Started
1. Clone Repository
git clone https://github.com/your-username/ai-devops-copilot.git
cd ai-devops-copilot
2. Install Dependencies
pip install -r requirements.txt
3. Run Backend (FastAPI)
uvicorn main:app --reload
4. Run Frontend (Streamlit)
streamlit run app.py
📌 API Example
Endpoint
POST /analyze
Request
{
  "log": "ERROR: Service unavailable",
  "metrics": {
    "cpu": "95%",
    "memory": "80%"
  }
}
Response
{
  "error": "Service Failure",
  "root_cause": "High CPU usage caused service crash",
  "suggested_fix": "Scale system or restart service",
  "action": "Simulated scaling executed"
}
📈 Key Features
AI-powered log and metric analysis
Agent-based decision making
Root cause detection
Intelligent fix suggestions
Self-healing simulation
Modular and scalable architecture
⚠️ Limitations
Uses simulated infrastructure actions
Depends on LLM accuracy
Limited real-time data streaming
🔮 Future Enhancements
Real Kubernetes-based auto-healing
Real-time log streaming integration
Slack/Email alert integration
Multi-agent orchestration
Historical learning using vector databases
🏆 Resume Highlight

Developed an AI-powered DevOps Copilot with agentic workflows that analyzes logs and metrics, performs root cause analysis, and simulates self-healing actions using FastAPI, LangGraph, and LLMs.

🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

📄 License

This project is licensed under the MIT License.
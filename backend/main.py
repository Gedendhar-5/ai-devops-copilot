from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.core.preprocessor import normalize, to_dataframe
from backend.agents.graph import run_graph
import os

load_dotenv()

app = FastAPI(
    title="AI DevOps Copilot",
    description="Agentic log analysis and self-healing simulation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class MetricsInput(BaseModel):
    cpu: str
    memory: str
    error_rate: str = "0%"


class AnalyzeRequest(BaseModel):
    log: str
    metrics: MetricsInput


class AnalyzeResponse(BaseModel):
    error_type:    str
    root_cause:    str
    suggested_fix: str
    action_taken:  str
    confidence:    str
    severity_tag:  str
    auto_resolved: bool


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "AI DevOps Copilot API is running", "docs": "/docs"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        normalized = normalize(
            log=request.log,
            cpu=request.metrics.cpu,
            memory=request.metrics.memory,
            error_rate=request.metrics.error_rate,
        )
        df = to_dataframe(normalized)
        print("\n--- Preprocessed input ---")
        print(df.to_string(index=False))

        print("\n--- Starting LangGraph pipeline ---")
        final_state = run_graph(normalized)
        print("\n--- Pipeline complete ---")

        return AnalyzeResponse(
            error_type=final_state["error_type"],
            root_cause=final_state["root_cause"],
            suggested_fix=final_state["suggested_fix"],
            action_taken=final_state["action_taken"],
            confidence=final_state["confidence"],
            severity_tag=final_state["severity_tag"],
            auto_resolved=final_state["auto_resolved"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from backend.core.preprocessor import NormalizedInput
from backend.core.llm import run_analysis, run_decision
from backend.core.decision_engine import execute, RemediationResult

load_dotenv()


class AgentState(TypedDict):
    normalized:       NormalizedInput
    error_type:       str
    root_cause:       str
    suggested_fix:    str
    confidence:       str
    action_label:     str
    action_taken:     str
    severity_tag:     str
    auto_resolved:    bool


def analyzer_agent(state: AgentState) -> AgentState:
    print("\n[Agent 1] Analyzer running...")
    analysis = run_analysis(state["normalized"])
    return {
        **state,
        "error_type":    analysis["error_type"],
        "root_cause":    analysis["root_cause"],
        "suggested_fix": analysis["suggested_fix"],
        "confidence":    analysis["confidence"],
    }


def decision_agent(state: AgentState) -> AgentState:
    print("\n[Agent 2] Decision running...")
    action_label = run_decision(
        error_type=state["error_type"],
        root_cause=state["root_cause"],
    )
    print(f"[Agent 2] LLM decision: {action_label}")
    return {
        **state,
        "action_label": action_label,
    }


def action_agent(state: AgentState) -> AgentState:
    print("\n[Agent 3] Action + Decision Engine running...")
    normalized = state["normalized"]

    # Decision Engine applies rules on top of LLM decision
    result: RemediationResult = execute(
        llm_action=state["action_label"],
        cpu=normalized.cpu_pct,
        memory=normalized.memory_pct,
        error_rate=normalized.error_rate_pct,
        keywords=normalized.parsed_log.keywords,
        severity=normalized.severity,
    )

    print(f"[Agent 3] Final action: {result.action_label}")
    print(f"[Agent 3] Severity: {result.severity_tag}")
    print(f"[Agent 3] Auto resolved: {result.auto_resolved}")

    return {
        **state,
        "action_taken":  result.action_taken,
        "severity_tag":  result.severity_tag,
        "auto_resolved": result.auto_resolved,
    }


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("analyzer", analyzer_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("action",   action_agent)
    graph.set_entry_point("analyzer")
    graph.add_edge("analyzer", "decision")
    graph.add_edge("decision", "action")
    graph.add_edge("action", END)
    return graph.compile()


DEVOPS_GRAPH = build_graph()


def run_graph(normalized: NormalizedInput) -> AgentState:
    initial_state: AgentState = {
        "normalized":    normalized,
        "error_type":    "",
        "root_cause":    "",
        "suggested_fix": "",
        "confidence":    "",
        "action_label":  "",
        "action_taken":  "",
        "severity_tag":  "",
        "auto_resolved": False,
    }
    return DEVOPS_GRAPH.invoke(initial_state)
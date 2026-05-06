import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from backend.core.preprocessor import NormalizedInput
from backend.core.prompts import build_analysis_prompt, build_decision_prompt

load_dotenv()


def _get_llm() -> ChatGroq:
    """Initializes the Groq LLM client. Called fresh each request — stateless."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.2,      # low temp = consistent, deterministic outputs
        max_tokens=512,
    )


def _parse_analysis_response(raw: str) -> dict:
    """
    Parses the strict-format LLM response into a dict.
    Falls back gracefully if the LLM doesn't follow the format exactly.
    """
    result = {
        "error_type": "Unknown",
        "root_cause": "Could not determine root cause",
        "suggested_fix": "Manual investigation required",
        "confidence": "Low",
    }

    patterns = {
        "error_type":    r"ERROR_TYPE:\s*(.+)",
        "root_cause":    r"ROOT_CAUSE:\s*(.+)",
        "suggested_fix": r"SUGGESTED_FIX:\s*(.+)",
        "confidence":    r"CONFIDENCE:\s*(.+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, raw, re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()

    return result


def run_analysis(normalized: NormalizedInput) -> dict:
    """
    Sends the incident data to the LLM and returns parsed root cause analysis.
    This is called by the Analyzer Agent in Phase 4.
    """
    llm = _get_llm()
    prompt = build_analysis_prompt(normalized)

    response = llm.invoke([HumanMessage(content=prompt)])
    raw_text = response.content

    print("\n--- LLM raw response ---")
    print(raw_text)

    return _parse_analysis_response(raw_text)


def run_decision(error_type: str, root_cause: str) -> str:
    """
    Asks the LLM to pick a remediation action label.
    Returns one of: 'restart', 'scale', 'alert'
    This is called by the Decision Agent in Phase 4.
    """
    llm = _get_llm()
    prompt = build_decision_prompt(error_type, root_cause)

    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content.strip().lower()

    # Defensive parse — only accept known actions
    for action in ["restart", "scale", "alert"]:
        if action in raw:
            return action

    return "alert"  # safe fallback
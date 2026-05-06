from dataclasses import dataclass


@dataclass
class RemediationResult:
    action_label: str       # restart / scale / alert
    action_taken: str       # human-readable simulation result
    severity_tag: str       # CRITICAL / HIGH / MEDIUM / LOW
    auto_resolved: bool     # True if simulated fix was applied


# --- Rule-based override layer ---
# If LLM decision conflicts with hard metric thresholds, rules win.
# This makes the system predictable and auditable.

RULES = [
    {
        "name": "critical_cpu_scale",
        "condition": lambda m, kw: m["cpu"] >= 90 and "timeout" in kw,
        "action": "scale",
    },
    {
        "name": "oom_restart",
        "condition": lambda m, kw: m["memory"] >= 90 or "crash" in kw or "memory" in kw,
        "action": "restart",
    },
    {
        "name": "high_error_rate_alert",
        "condition": lambda m, kw: m["error_rate"] >= 50,
        "action": "alert",
    },
    {
        "name": "db_issue_alert",
        "condition": lambda m, kw: "database" in kw,
        "action": "alert",
    },
    {
        "name": "high_cpu_scale",
        "condition": lambda m, kw: m["cpu"] >= 75,
        "action": "scale",
    },
]


SIMULATIONS = {
    "restart": "Simulated: Service restarted — pod recycled and health check passed",
    "scale":   "Simulated: System scaled — replicas increased from 2 to 4",
    "alert":   "Simulated: Alert sent to DevOps team via PagerDuty",
}

SEVERITY_TAGS = {
    "critical": "🔴 CRITICAL",
    "high":     "🟠 HIGH",
    "medium":   "🟡 MEDIUM",
    "low":      "🟢 LOW",
}


def apply_rules(
    llm_action: str,
    cpu: float,
    memory: float,
    error_rate: float,
    keywords: list[str],
) -> str:
    """
    Runs rule-based checks against metrics and keywords.
    If any rule matches, it overrides the LLM decision.
    Returns the final action label.
    """
    metrics = {"cpu": cpu, "memory": memory, "error_rate": error_rate}

    for rule in RULES:
        if rule["condition"](metrics, keywords):
            final = rule["action"]
            if final != llm_action:
                print(f"[DecisionEngine] Rule '{rule['name']}' overrides LLM '{llm_action}' → '{final}'")
            return final

    # No rule matched — trust the LLM
    return llm_action


def execute(
    llm_action: str,
    cpu: float,
    memory: float,
    error_rate: float,
    keywords: list[str],
    severity: str,
) -> RemediationResult:
    """
    Main entry point for the Decision Engine.
    Applies rules, runs simulation, returns full RemediationResult.
    """
    final_action = apply_rules(llm_action, cpu, memory, error_rate, keywords)
    action_taken = SIMULATIONS.get(final_action, SIMULATIONS["alert"])
    severity_tag = SEVERITY_TAGS.get(severity, "🟡 MEDIUM")
    auto_resolved = final_action in ["restart", "scale"]

    return RemediationResult(
        action_label=final_action,
        action_taken=action_taken,
        severity_tag=severity_tag,
        auto_resolved=auto_resolved,
    )
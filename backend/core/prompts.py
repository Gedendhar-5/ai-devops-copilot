import re
from backend.core.preprocessor import NormalizedInput


def build_analysis_prompt(normalized: NormalizedInput) -> str:
    log = normalized.parsed_log
    return f"""You are a senior DevOps engineer analyzing a production incident.

## Incident Data

**Log entry:**
{log.raw}

**Parsed details:**
- Level: {log.level}
- Service: {log.service}
- Pod: {log.pod or 'N/A'}
- Detected keywords: {', '.join(log.keywords) or 'none'}

**System metrics:**
- CPU usage: {normalized.cpu_pct}%
- Memory usage: {normalized.memory_pct}%
- Error rate: {normalized.error_rate_pct}%
- Severity: {normalized.severity}

## Your Task

Analyze this incident and respond in EXACTLY this format - no extra text, no markdown, no preamble:

ERROR_TYPE: <one short phrase, e.g. Connection Timeout or OOM Crash>
ROOT_CAUSE: <1-2 sentences explaining why this happened based on the metrics and log>
SUGGESTED_FIX: <1-2 sentences on how to fix it>
CONFIDENCE: <High / Medium / Low>
"""


def build_decision_prompt(error_type: str, root_cause: str) -> str:
    return f"""You are a DevOps automation system.

Given this incident:
- Error type: {error_type}
- Root cause: {root_cause}

Respond with EXACTLY one word - the action to take:
- restart   (use when: service crash, process killed, fatal error)
- scale     (use when: high CPU, timeout, connection pool exhausted)
- alert     (use when: high error rate, unknown issue, needs human review)

Your response must be one word only: restart, scale, or alert
"""

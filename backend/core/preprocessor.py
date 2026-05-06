import re
import pandas as pd
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedLog:
    raw: str
    level: str
    service: str
    error_message: str
    pod: Optional[str]
    keywords: list[str]


@dataclass
class NormalizedInput:
    parsed_log: ParsedLog
    cpu_pct: float
    memory_pct: float
    error_rate_pct: float
    severity: str


LEVEL_RE     = re.compile(r"\b(ERROR|WARN|WARNING|CRITICAL|INFO|FATAL)\b", re.IGNORECASE)
SERVICE_RE   = re.compile(r"[Ss]ervice[:\s]+([a-zA-Z0-9_-]+)")
POD_RE       = re.compile(r"[Pp]od[:\s]+([a-zA-Z0-9_-]+)")
PERCENT_RE   = re.compile(r"(\d+(?:\.\d+)?)%")

KEYWORD_PATTERNS = {
    "timeout":     re.compile(r"\b(timeout|timed?\s*out)\b", re.IGNORECASE),
    "memory":      re.compile(r"\b(out of memory|oom|memory)\b", re.IGNORECASE),
    "crash":       re.compile(r"\b(crash|crashed|killed|fatal)\b", re.IGNORECASE),
    "cpu":         re.compile(r"\b(cpu|throttl)\b", re.IGNORECASE),
    "connection":  re.compile(r"\b(connection|connect|refused|unreachable)\b", re.IGNORECASE),
    "unavailable": re.compile(r"\b(unavailable|503|502|down)\b", re.IGNORECASE),
    "database":    re.compile(r"\b(database|db|pool|postgres|mysql|mongo)\b", re.IGNORECASE),
}


def _extract_percent(value: str) -> float:
    match = PERCENT_RE.search(str(value))
    return float(match.group(1)) if match else 0.0


def _compute_severity(cpu: float, memory: float, error_rate: float) -> str:
    if cpu >= 90 or memory >= 90 or error_rate >= 50:
        return "critical"
    if cpu >= 75 or memory >= 75 or error_rate >= 25:
        return "high"
    if cpu >= 50 or memory >= 50 or error_rate >= 10:
        return "medium"
    return "low"


def parse_log(raw_log: str) -> ParsedLog:
    raw_log = raw_log.strip()
    level_match   = LEVEL_RE.search(raw_log)
    service_match = SERVICE_RE.search(raw_log)
    pod_match     = POD_RE.search(raw_log)

    level   = level_match.group(1).upper() if level_match   else "UNKNOWN"
    service = service_match.group(1)        if service_match else "unknown"
    pod     = pod_match.group(1)            if pod_match     else None
    cleaned = LEVEL_RE.sub("", raw_log).strip(" :-")
    keywords = [kw for kw, pattern in KEYWORD_PATTERNS.items() if pattern.search(raw_log)]

    return ParsedLog(
        raw=raw_log,
        level=level,
        service=service,
        error_message=cleaned,
        pod=pod,
        keywords=keywords,
    )


def normalize(log: str, cpu: str, memory: str, error_rate: str) -> NormalizedInput:
    parsed     = parse_log(log)
    cpu_pct    = _extract_percent(cpu)
    mem_pct    = _extract_percent(memory)
    err_pct    = _extract_percent(error_rate)
    severity   = _compute_severity(cpu_pct, mem_pct, err_pct)

    return NormalizedInput(
        parsed_log=parsed,
        cpu_pct=cpu_pct,
        memory_pct=mem_pct,
        error_rate_pct=err_pct,
        severity=severity,
    )


def to_dataframe(normalized: NormalizedInput) -> pd.DataFrame:
    log = normalized.parsed_log
    return pd.DataFrame([{
        "level":      log.level,
        "service":    log.service,
        "pod":        log.pod or "N/A",
        "message":    log.error_message,
        "keywords":   ", ".join(log.keywords),
        "cpu_pct":    normalized.cpu_pct,
        "memory_pct": normalized.memory_pct,
        "error_rate": normalized.error_rate_pct,
        "severity":   normalized.severity,
    }])
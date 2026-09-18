from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score, tuned for a dark page."""
    if score >= 80:
        return "#4ADE80", "#132A1D"  # green
    if score >= 60:
        return "#FBBF24", "#2A2113"  # amber
    return "#F87171", "#2A1616"      # red


def get_score_label(score: float) -> str:
    """Short text label that matches the score band — used in headlines."""
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Needs Work"
    return "Weak"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """
    Return (label, text_color, background_color) for an IssueDetail severity,
    tuned for a dark page.
    Matches the values the backend emits in `detailed_feedback[].severity_level`.
    """
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return level.upper(), "#F87171", "#2A1616"
    if level == "medium":
        return "MEDIUM", "#FBBF24", "#2A2113"
    return "LOW", "#4ADE80", "#132A1D"
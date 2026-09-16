from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score."""
    if score >= 80:
        return "#15803D", "#F0FDF4"  # green
    if score >= 60:
        return "#B45309", "#FFFBEB"  # amber
    return "#B91C1C", "#FEF2F2"      # red


def get_score_label(score: float) -> str:
    """Short text label that matches the score band — used in headlines."""
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Needs Work"
    return "Weak"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """
    Return (label, text_color, background_color) for an IssueDetail severity.
    Matches the values the backend emits in `detailed_feedback[].severity_level`.
    """
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return level.upper(), "#B91C1C", "#FEF2F2"
    if level == "medium":
        return "MEDIUM", "#B45309", "#FFFBEB"
    return "LOW", "#15803D", "#F0FDF4"

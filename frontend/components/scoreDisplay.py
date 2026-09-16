from typing import Any, Dict

import streamlit as st

from frontend.components._helper import get_score_color, get_score_label


# Component max scores match backend/core/config.py SCORE_WEIGHTS.
# (Backend returns each component's score on its own scale, not 0–100.)
COMPONENTS = [
    ("Formatting",        "formatting",        20),
    ("Keywords & Skills", "keywords",          25),
    ("Content Quality",   "content",           25),
    ("Skill Validation",  "skill_validation",  15),
    ("ATS Compatibility", "ats_compatibility", 15),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    """Score card with a short interpretation line."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    text_color, bg_color = get_score_color(score)
    label = get_score_label(score)

    st.markdown("## Analysis Results")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            f"""
            <div style="text-align:center; padding:1.75rem; background-color:{bg_color};
                        border:1px solid {text_color}22; border-radius:8px;">
                <h1 style="color:{text_color}; font-size:3.5rem; margin:0; font-weight:700;">
                    {score:.0f}
                </h1>
                <p style="color:{text_color}; margin:0.25rem 0 0; font-weight:600;
                          letter-spacing:0.03em; font-size:0.85rem; text-transform:uppercase;">
                    {label} — Overall ATS Score
                </p>
                <p style="color:#6B7280; margin-top:0.75rem;">{interpretation}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    """Five progress bars, one per scoring component."""
    component_scores = analysis.get("component_scores") or {}
    st.markdown("### Score Breakdown")

    left, right = st.columns(2)
    for i, (label, key, max_score) in enumerate(COMPONENTS):
        value = float(component_scores.get(key, 0))
        percentage = value / max_score if max_score else 0
        bar_color = "#15803D" if percentage >= 0.8 else "#B45309" if percentage >= 0.6 else "#B91C1C"

        with left if i % 2 == 0 else right:
            st.markdown(f"**{label}**")
            st.markdown(
                f"""
                <div style="background-color:#E5E7EB; border-radius:4px; height:10px; margin-bottom:5px;">
                    <div style="background-color:{bar_color}; width:{percentage * 100}%;
                                height:100%; border-radius:4px;"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"**{value:.0f}/{max_score}**")
            st.markdown("")

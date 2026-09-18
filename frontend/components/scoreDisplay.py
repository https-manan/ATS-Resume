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
    """Plain stat-row card: big number, label, short interpretation."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    text_color, _ = get_score_color(score)
    label = get_score_label(score)

    st.markdown("## Analysis Results")
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:1.5rem; background:#1C1F26;
                    border:1px solid #30343C; border-left:4px solid {text_color};
                    border-radius:8px; padding:1.25rem 1.5rem;">
            <div style="font-size:3rem; font-weight:700; color:{text_color}; min-width:90px;">
                {score:.0f}
            </div>
            <div>
                <div style="font-weight:700; color:{text_color}; text-transform:uppercase;
                            font-size:0.8rem; letter-spacing:0.03em;">
                    {label} — Overall ATS Score
                </div>
                <div style="color:#B5B9C0; margin-top:0.35rem;">{interpretation}</div>
            </div>
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
        bar_color = "#4ADE80" if percentage >= 0.8 else "#FBBF24" if percentage >= 0.6 else "#F87171"

        with left if i % 2 == 0 else right:
            st.markdown(f"**{label}**")
            st.markdown(
                f"""
                <div style="background-color:#30343C; border-radius:4px; height:10px; margin-bottom:5px;">
                    <div style="background-color:{bar_color}; width:{percentage * 100}%;
                                height:100%; border-radius:4px;"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"**{value:.0f}/{max_score}**")
            st.markdown("")
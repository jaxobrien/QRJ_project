import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Regression coefficients — sourced directly from Appendix 2, "All data" column
# We use a composite additive model combining the key interaction models.
# Intercept anchored from the health model (most complete single-predictor base).
# ---------------------------------------------------------------------------
INTERCEPT = 4.629

COEFS = {
    "online_hrs":                  -0.267,
    "health":                       0.338,
    "online_hrs_x_health":          0.037,
    "selfesteem_index":             1.081,
    "online_hrs_x_selfesteem":      0.067,
    "sdq_total":                   -0.082,
    "online_hrs_x_sdq":            -0.004,
    "sex":                          0.090,
    "online_hrs_x_sex":            -0.120,
    "parent_index":                 0.128,
    "online_hrs_x_parent":          0.026,
}

ONLINE_HRS_LABELS = ["None (0)", "<1 hour (1)", "1–3 hours (2)", "4–6 hours (3)", "7+ hours (4)"]
ONLINE_HRS_VALUES = [0, 1, 2, 3, 4]

HEALTH_LABELS = ["Poor (1)", "Fair (2)", "Good (3)", "Very good (4)", "Excellent (5)"]
HEALTH_VALUES = [1, 2, 3, 4, 5]


def estimate_happiness(online_hrs, health, selfesteem, sdq, sex, parent):
    """
    Compute predicted happiness from appendix regression coefficients.
    Clamps output to the 1–7 scale.
    """
    score = (
        INTERCEPT
        + COEFS["online_hrs"] * online_hrs
        + COEFS["health"] * health
        + COEFS["online_hrs_x_health"] * online_hrs * health
        + COEFS["selfesteem_index"] * selfesteem
        + COEFS["online_hrs_x_selfesteem"] * online_hrs * selfesteem
        + COEFS["sdq_total"] * sdq
        + COEFS["online_hrs_x_sdq"] * online_hrs * sdq
        + COEFS["sex"] * sex
        + COEFS["online_hrs_x_sex"] * online_hrs * sex
        + COEFS["parent_index"] * parent
        + COEFS["online_hrs_x_parent"] * online_hrs * parent
    )
    return round(max(1.0, min(7.0, score)), 2)


def happiness_label(score):
    if score >= 6.5:
        return "Very happy"
    elif score >= 5.5:
        return "Fairly happy"
    elif score >= 4.5:
        return "Somewhat unhappy"
    else:
        return "Unhappy"


def happiness_colour(score):
    if score >= 6.5:
        return "#2ECC71"
    elif score >= 5.5:
        return "#4C9BE8"
    elif score >= 4.5:
        return "#E8B44C"
    else:
        return "#E8714C"


def build_gauge(score):
    colour = happiness_colour(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 7", "font": {"size": 28, "family": "Arial"}},
        gauge={
            "axis": {
                "range": [1, 7],
                "tickvals": [1, 2, 3, 4, 5, 6, 7],
                "ticktext": ["1", "2", "3", "4", "5", "6", "7"],
            },
            "bar": {"color": colour, "thickness": 0.25},
            "bgcolor": "#F5F5F5",
            "steps": [
                {"range": [1, 4.5], "color": "#FFE5DE"},
                {"range": [4.5, 5.5], "color": "#FFF3DE"},
                {"range": [5.5, 6.5], "color": "#DEF0FF"},
                {"range": [6.5, 7],   "color": "#DEFFED"},
            ],
            "threshold": {
                "line": {"color": "#333333", "width": 2},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        height=260,
        margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif"),
    )
    return fig


def render_widget():
    """Render the full risk profile widget in Streamlit."""

    st.markdown("### Risk profile estimator")
    st.markdown(
        "Adjust the characteristics below to see the estimated happiness score "
        "for an adolescent with that profile. Estimates are derived from regression "
        "models fitted to survey data from 4,595 UK adolescents aged 10–15 "
        "(Understanding Society, 2010–2019). This is a statistical estimate based "
        "on group-level data — not a diagnostic tool."
    )

    col_l, col_r = st.columns([1, 1])

    with col_l:
        sex_input = st.radio("Sex", ["Boy", "Girl"], horizontal=True)
        sex_val = 1 if sex_input == "Girl" else 0

        online_label = st.select_slider(
            "Daily social media use (weekdays)",
            options=ONLINE_HRS_LABELS,
            value=ONLINE_HRS_LABELS[1],
        )
        online_val = ONLINE_HRS_VALUES[ONLINE_HRS_LABELS.index(online_label)]

        health_label = st.select_slider(
            "Self-reported physical health",
            options=HEALTH_LABELS,
            value=HEALTH_LABELS[2],
        )
        health_val = HEALTH_VALUES[HEALTH_LABELS.index(health_label)]

    with col_r:
        selfesteem_val = st.slider(
            "Self-esteem (1 = lowest, 4 = highest)",
            min_value=1.0, max_value=4.0, value=3.1, step=0.1,
        )
        sdq_val = st.slider(
            "Mental health difficulties score (0 = none, 32 = severe)",
            min_value=0, max_value=32, value=11,
        )
        parent_val = st.slider(
            "Parental support (1 = lowest, 4 = highest)",
            min_value=1.0, max_value=4.0, value=3.0, step=0.1,
        )

    score = estimate_happiness(
        online_hrs=online_val,
        health=health_val,
        selfesteem=selfesteem_val,
        sdq=sdq_val,
        sex=sex_val,
        parent=parent_val,
    )

    label = happiness_label(score)
    colour = happiness_colour(score)

    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        st.plotly_chart(build_gauge(score), use_container_width=True)

    with res_col2:
        st.markdown(f"<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='color:{colour};'>{label}</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"Estimated happiness score: **{score} / 7**  \n"
            f"The scale runs from *Not at all happy* (1) to *Completely happy* (7)."
        )

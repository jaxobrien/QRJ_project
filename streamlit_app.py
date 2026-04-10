import streamlit as st
from utils.data_loader import load_panels, build_moderator_data
from utils.charts.panel_overview import build_chart1
from utils.charts.moderator_toggle import build_chart2
from utils.charts.risk_profile_widget import render_widget
from style import apply_styles, style_fig, pull_quote, finding_card, section_rule, app_footer

# apply_styles() calls st.set_page_config internally
apply_styles()

# ---------------------------------------------------------------------------
# Load data once and cache
# ---------------------------------------------------------------------------
@st.cache_data
def get_data():
    df1, df2, df_combined = load_panels()
    mod_data = build_moderator_data(df_combined)
    return df1, df2, df_combined, mod_data

df1, df2, df_combined, mod_data = get_data()

# ---------------------------------------------------------------------------
# Per-moderator caption metadata
# All values sourced directly from Appendix 2.
# b_int = interaction coefficient (online_hrs x moderator)
# se    = standard error of b_int
# p_sig = significance derived from z = |b_int / SE|
# n     = observations in interaction model
# r2    = R-squared of interaction model
# ---------------------------------------------------------------------------
MOD_CAPTIONS = {
    "Sex": {
        "levels": "Binary: 0 = Male, 1 = Female.",
        "p1": {
            "b_int": -0.095, "se": 0.046, "p_sig": "p < 0.05 *",
            "n": 1907, "r2": 0.040,
            "note": (
                "Each additional bracket of weekday social media use is associated with "
                "a 0.095-point steeper decline in happiness for girls than boys."
            ),
        },
        "p2": {
            "b_int": -0.121, "se": 0.054, "p_sig": "p < 0.05 *",
            "n": 1533, "r2": 0.052,
            "note": (
                "The gender gap widened in the later panel: girls experienced a "
                "0.121-point greater per-bracket decline than boys."
            ),
        },
    },
    "Self-esteem": {
        "levels": (
            "Composite index 1-4 (1 = least positive, 4 = most positive), "
            "built from 8 Rosenberg-style items. Cronbach alpha = 0.79."
        ),
        "p1": {
            "b_int": 0.089, "se": 0.064, "p_sig": "p = n.s.",
            "n": 793, "r2": 0.361,
            "note": (
                "In Panel 1, self-esteem did not significantly moderate the SM-happiness "
                "relationship, though higher self-esteem was strongly protective overall."
            ),
        },
        "p2": {
            "b_int": 0.157, "se": 0.048, "p_sig": "p < 0.01 **",
            "n": 906, "r2": 0.472,
            "note": (
                "By Panel 2 the interaction was significant: adolescents with higher "
                "self-esteem showed less decline per SM bracket (buffering effect)."
            ),
        },
    },
    "SDQ": {
        "levels": (
            "SDQ Total Difficulties Score grouped into clinical bands: "
            "Normal (0-15), Borderline (16-19), Abnormal (20-40). "
            "Higher scores = greater psychological difficulties. "
            "Borderline and abnormal groups are small; interpret with caution."
        ),
        "p1": {
            "b_int": -0.010, "se": 0.004, "p_sig": "p < 0.05 *",
            "n": 1104, "r2": 0.372,
            "note": (
                "In Panel 1, greater psychological difficulties amplified the negative "
                "effect of SM use on happiness (b = -0.010 per SDQ point per SM bracket)."
            ),
        },
        "p2": {
            "b_int": 0.000, "se": 0.005, "p_sig": "p = n.s.",
            "n": 624, "r2": 0.433,
            "note": (
                "In Panel 2 the interaction was not significant; the baseline disadvantage "
                "of higher SDQ scores remained but did not compound with SM use."
            ),
        },
    },
    "Physical health": {
        "levels": (
            "Self-rated health: 1 = Poor, 2 = Fair, 3 = Good, "
            "4 = Very good, 5 = Excellent. Shown at all five integer levels."
        ),
        "p1": {
            "b_int": 0.077, "se": 0.037, "p_sig": "p < 0.05 *",
            "n": 784, "r2": 0.149,
            "note": (
                "Better physical health buffered the SM-happiness association: each step up "
                "the health scale reduced the per-bracket happiness decline by 0.077 points."
            ),
        },
        "p2": {
            "b_int": 0.097, "se": 0.033, "p_sig": "p < 0.01 **",
            "n": 903, "r2": 0.244,
            "note": (
                "The buffering effect strengthened in Panel 2 (b = +0.097, p < 0.01): "
                "adolescents in excellent health were substantially more resilient to heavy SM use."
            ),
        },
    },
    "Parental relationship": {
        "levels": (
            "Composite index 1-4 (1 = least positive, 4 = most positive), built from "
            "7 items covering arguments, communication, shared meals, and parental interest. "
            "Cronbach alpha = 0.55; low internal consistency reflects conceptually distinct dimensions."
        ),
        "p1": {
            "b_int": 0.011, "se": 0.028, "p_sig": "p = n.s.",
            "n": 1902, "r2": 0.050,
            "note": (
                "Parental relationship did not significantly moderate the SM-happiness "
                "link in Panel 1, though positive relationships predicted higher happiness overall."
            ),
        },
        "p2": {
            "b_int": 0.062, "se": 0.031, "p_sig": "p < 0.05 *",
            "n": 1532, "r2": 0.070,
            "note": (
                "By Panel 2 a significant buffering effect emerged: adolescents with the "
                "most positive parental relationships showed less SM-related happiness decline."
            ),
        },
    },
    "Sibling relationship": {
        "levels": (
            "Composite index 1-4 (1 = least positive, 4 = most positive), built from "
            "8 items capturing both victimisation and perpetration of inter-sibling conflict. "
            "Cronbach alpha = 0.88. Only participants with siblings in the household are included."
        ),
        "p1": {
            "b_int": 0.013, "se": 0.041, "p_sig": "p = n.s.",
            "n": 990, "r2": 0.098,
            "note": (
                "Sibling relationship quality did not significantly interact with SM use in Panel 1."
            ),
        },
        "p2": {
            "b_int": -0.191, "se": 0.058, "p_sig": "p < 0.001 ***",
            "n": 552, "r2": 0.107,
            "note": (
                "A striking reversal in Panel 2: adolescents with more positive sibling "
                "relationships showed a stronger negative SM-happiness association "
                "(b = -0.191, p < 0.001). This counterintuitive finding warrants caution "
                "given the smaller sample (N = 552)."
            ),
        },
    },
    "Leisure activity": {
        "levels": (
            "Composite index 0-5, mean of 16 leisure items (cinema, sport, volunteering, etc.). "
            "Scale: 0 = Never/almost never to 5 = Most days. "
            "Cronbach alpha = 0.66; items reflect breadth of engagement rather than a single construct."
        ),
        "p1": {
            "b_int": -0.043, "se": 0.034, "p_sig": "p = n.s.",
            "n": 1000, "r2": 0.044,
            "note": "No significant moderation in Panel 1.",
        },
        "p2": {
            "b_int": 0.095, "se": 0.066, "p_sig": "p = n.s.",
            "n": 907, "r2": 0.091,
            "note": (
                "No significant moderation in Panel 2 either. The point estimate reversed "
                "direction but the wide standard error (SE = 0.066) indicates high uncertainty."
            ),
        },
    },
    "Bullying involvement": {
        "levels": (
            "Binary composite: 1 = any involvement in bullying (as victim or perpetrator) "
            "across four items (physical/other, victim/perpetrator). "
            "Original ordinal scales recoded to binary due to highly skewed distributions."
        ),
        "p1": {
            "b_int": -0.128, "se": 0.109, "p_sig": "p = n.s.",
            "n": 1104, "r2": 0.150,
            "note": (
                "No significant moderation in Panel 1, though involved adolescents reported "
                "substantially lower baseline happiness (b_mod = -0.864)."
            ),
        },
        "p2": {
            "b_int": 0.161, "se": 0.169, "p_sig": "p = n.s.",
            "n": 626, "r2": 0.151,
            "note": (
                "No significant interaction in Panel 2. Wide confidence bands reflect "
                "limited precision; the bullying subgroup is small and estimates are imprecise."
            ),
        },
    },
}

# Map display label to mod_data key — order must match build_moderator_data output
LABEL_TO_KEY = {
    "Sex":                   "sex",
    "Self-esteem":           "selfesteem",
    "SDQ":                   "sdq",
    "Physical health":       "health",
    "Parental relationship": "parent",
    "Sibling relationship":  "siblings",
    "Leisure activity":      "leisure",
    "Bullying involvement":  "bullying",
}

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("Social Media & Adolescent Happiness")
st.markdown(
    "How does daily social media use relate to the happiness of UK adolescents "
    "aged 10 to 15 -- and who is most at risk?"
)

section_rule()

# ---------------------------------------------------------------------------
# Section 1: Overview chart
# ---------------------------------------------------------------------------
st.subheader("Happiness falls as social media use rises")
st.markdown(
    "Across both panels, mean happiness declines steadily from age 10 to 15, "
    "while weekday social media use increases. The gap between the two cohorts "
    "widens with age, with adolescents in the 2015-2019 panel spending more time "
    "online and reporting lower happiness by age 15."
)
st.plotly_chart(
    style_fig(build_chart1(df1, df2)),
    use_container_width=True,
)
st.caption(
    "Source: Understanding Society (UK Household Longitudinal Study), waves 2010-2019. "
    "N = 919 unique participants across both panels. Ages 10-15 only."
)

section_rule()

# ---------------------------------------------------------------------------
# Section 2: Moderator toggle + dynamic caption
# ---------------------------------------------------------------------------
st.subheader("Who is most affected?")
st.markdown(
    "The relationship between social media use and happiness is not the same for "
    "everyone. Select a moderating factor to explore how individual characteristics "
    "shape that relationship across both panel cohorts. "
    "Shaded bands show 95% confidence intervals around predicted values."
)

# Radio rendered as a horizontal button row — drives both chart and caption
selected_label = st.radio(
    "Moderating factor",
    options=list(LABEL_TO_KEY.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

# Determine which index is selected so we can pre-set trace visibility
mod_keys_ordered = list(LABEL_TO_KEY.keys())
selected_index = mod_keys_ordered.index(selected_label)

# Build chart
fig2 = build_chart2(mod_data)

# Compute trace visibility to match the selected moderator
traces_per_mod = []
for key in LABEL_TO_KEY.values():
    n_groups = len(mod_data[key]["groups"])
    traces_per_mod.append(n_groups * 4)  # 2 traces (band+line) x 2 panels = 4 per group

total_traces = sum(traces_per_mod)
vis = [False] * total_traces
sl  = [False] * total_traces
offset = sum(traces_per_mod[:selected_index])
n_traces = traces_per_mod[selected_index]
n_groups = len(mod_data[list(LABEL_TO_KEY.values())[selected_index]]["groups"])

for j in range(n_traces):
    vis[offset + j] = True
for j in range(n_groups):
    sl[offset + j * 2 + 1] = True  # p1 line traces only (odd indices within p1 block)

for i, trace in enumerate(fig2.data):
    trace.visible = vis[i]
    if hasattr(trace, "showlegend"):
        trace.showlegend = sl[i]

st.plotly_chart(
    style_fig(fig2),
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# Dynamic caption — unique per moderator, sourced from Appendix 2
# ---------------------------------------------------------------------------
cap = MOD_CAPTIONS[selected_label]
p1  = cap["p1"]
p2  = cap["p2"]

st.caption(
    f"Moderator: {selected_label}. "
    f"{cap['levels']} "
    f"| Panel 1 (2010-14): interaction coefficient b = {p1['b_int']:+.3f} "
    f"(SE = {p1['se']:.3f}), {p1['p_sig']}, N = {p1['n']:,}, R² = {p1['r2']:.3f}. "
    f"{p1['note']} "
    f"| Panel 2 (2015-19): interaction coefficient b = {p2['b_int']:+.3f} "
    f"(SE = {p2['se']:.3f}), {p2['p_sig']}, N = {p2['n']:,}, R² = {p2['r2']:.3f}. "
    f"{p2['note']} "
    f"| Confidence bands: +/-1.96 x SE(b_int) x SM hours x moderator value. "
    f"Source: Understanding Society (UKHLS), waves 2010-2019."
)

section_rule()

# ---------------------------------------------------------------------------
# Section 3: Risk profile widget
# ---------------------------------------------------------------------------
render_widget()

app_footer()

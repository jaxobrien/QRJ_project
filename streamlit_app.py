import streamlit as st
from utils.data_loader import load_panels, build_moderator_data
from utils.charts.panel_overview import build_chart1
from utils.charts.moderator_toggle import build_chart2
from utils.charts.risk_profile_widget import render_widget
from style import apply_styles, style_fig, section_rule, app_footer

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
# Scrapbook button config — shape, colour, text colour per moderator
# ---------------------------------------------------------------------------
BUTTON_CONFIG = {
    "Sex":                   {"shape": "heart",     "bg": "#e69c67", "fg": "#27304a"},
    "Self-esteem":           {"shape": "cloud",     "bg": "#fdf489", "fg": "#27304a"},
    "SDQ":                   {"shape": "banner",    "bg": "#2e4b62", "fg": "#fefdf9"},
    "Physical health":       {"shape": "starburst", "bg": "#97c58a", "fg": "#fefdf9"},
    "Parental relationship": {"shape": "heart",     "bg": "#ebc8bb", "fg": "#27304a"},
    "Sibling relationship":  {"shape": "cloud",     "bg": "#fdf489", "fg": "#27304a"},
    "Leisure activity":      {"shape": "banner",    "bg": "#27304a", "fg": "#fefdf9"},
    "Bullying involvement":  {"shape": "starburst", "bg": "#97c58a", "fg": "#27304a"},
}

# ---------------------------------------------------------------------------
# Per-moderator caption metadata (Appendix 2)
# ---------------------------------------------------------------------------
MOD_CAPTIONS = {
    "Sex": {
        "levels": "Binary: 0 = Male, 1 = Female.",
        "p1": {"b_int": -0.095, "se": 0.046, "p_sig": "p < 0.05 *",  "n": 1907, "r2": 0.040,
               "note": "Each additional bracket of weekday social media use is associated with a 0.095-point steeper decline in happiness for girls than boys."},
        "p2": {"b_int": -0.121, "se": 0.054, "p_sig": "p < 0.05 *",  "n": 1533, "r2": 0.052,
               "note": "The gender gap widened in the later panel: girls experienced a 0.121-point greater per-bracket decline than boys."},
    },
    "Self-esteem": {
        "levels": "Composite index 1-4 (1 = least positive, 4 = most positive), built from 8 Rosenberg-style items. Cronbach alpha = 0.79.",
        "p1": {"b_int":  0.089, "se": 0.064, "p_sig": "p = n.s.",    "n":  793, "r2": 0.361,
               "note": "In Panel 1, self-esteem did not significantly moderate the SM-happiness relationship, though higher self-esteem was strongly protective overall."},
        "p2": {"b_int":  0.157, "se": 0.048, "p_sig": "p < 0.01 **", "n":  906, "r2": 0.472,
               "note": "By Panel 2 the interaction was significant: adolescents with higher self-esteem showed less decline per SM bracket (buffering effect)."},
    },
    "SDQ": {
        "levels": "SDQ Total Difficulties Score grouped into clinical bands: Normal (0-15), Borderline (16-19), Abnormal (20-40). Higher scores = greater psychological difficulties. Borderline and abnormal groups are small; interpret with caution.",
        "p1": {"b_int": -0.010, "se": 0.004, "p_sig": "p < 0.05 *",  "n": 1104, "r2": 0.372,
               "note": "In Panel 1, greater psychological difficulties amplified the negative effect of SM use on happiness (b = -0.010 per SDQ point per SM bracket)."},
        "p2": {"b_int":  0.000, "se": 0.005, "p_sig": "p = n.s.",    "n":  624, "r2": 0.433,
               "note": "In Panel 2 the interaction was not significant; the baseline disadvantage of higher SDQ scores remained but did not compound with SM use."},
    },
    "Physical health": {
        "levels": "Self-rated health: 1 = Poor, 2 = Fair, 3 = Good, 4 = Very good, 5 = Excellent. Shown at all five integer levels.",
        "p1": {"b_int":  0.077, "se": 0.037, "p_sig": "p < 0.05 *",  "n":  784, "r2": 0.149,
               "note": "Better physical health buffered the SM-happiness association: each step up the health scale reduced the per-bracket happiness decline by 0.077 points."},
        "p2": {"b_int":  0.097, "se": 0.033, "p_sig": "p < 0.01 **", "n":  903, "r2": 0.244,
               "note": "The buffering effect strengthened in Panel 2 (b = +0.097, p < 0.01): adolescents in excellent health were substantially more resilient to heavy SM use."},
    },
    "Parental relationship": {
        "levels": "Composite index 1-4 (1 = least positive, 4 = most positive), built from 7 items covering arguments, communication, shared meals, and parental interest. Cronbach alpha = 0.55; low internal consistency reflects conceptually distinct dimensions.",
        "p1": {"b_int":  0.011, "se": 0.028, "p_sig": "p = n.s.",    "n": 1902, "r2": 0.050,
               "note": "Parental relationship did not significantly moderate the SM-happiness link in Panel 1, though positive relationships predicted higher happiness overall."},
        "p2": {"b_int":  0.062, "se": 0.031, "p_sig": "p < 0.05 *",  "n": 1532, "r2": 0.070,
               "note": "By Panel 2 a significant buffering effect emerged: adolescents with the most positive parental relationships showed less SM-related happiness decline."},
    },
    "Sibling relationship": {
        "levels": "Composite index 1-4 (1 = least positive, 4 = most positive), built from 8 items capturing both victimisation and perpetration of inter-sibling conflict. Cronbach alpha = 0.88. Only participants with siblings in the household are included.",
        "p1": {"b_int":  0.013, "se": 0.041, "p_sig": "p = n.s.",    "n":  990, "r2": 0.098,
               "note": "Sibling relationship quality did not significantly interact with SM use in Panel 1."},
        "p2": {"b_int": -0.191, "se": 0.058, "p_sig": "p < 0.001 ***", "n": 552, "r2": 0.107,
               "note": "A striking reversal in Panel 2: adolescents with more positive sibling relationships showed a stronger negative SM-happiness association (b = -0.191, p < 0.001). This counterintuitive finding warrants caution given the smaller sample (N = 552)."},
    },
    "Leisure activity": {
        "levels": "Composite index 0-5, mean of 16 leisure items (cinema, sport, volunteering, etc.). Scale: 0 = Never/almost never to 5 = Most days. Cronbach alpha = 0.66.",
        "p1": {"b_int": -0.043, "se": 0.034, "p_sig": "p = n.s.",    "n": 1000, "r2": 0.044,
               "note": "No significant moderation in Panel 1."},
        "p2": {"b_int":  0.095, "se": 0.066, "p_sig": "p = n.s.",    "n":  907, "r2": 0.091,
               "note": "No significant moderation in Panel 2 either. The point estimate reversed direction but the wide standard error (SE = 0.066) indicates high uncertainty."},
    },
    "Bullying involvement": {
        "levels": "Binary composite: 1 = any involvement in bullying (as victim or perpetrator) across four items (physical/other, victim/perpetrator). Original ordinal scales recoded to binary due to highly skewed distributions.",
        "p1": {"b_int": -0.128, "se": 0.109, "p_sig": "p = n.s.",    "n": 1104, "r2": 0.150,
               "note": "No significant moderation in Panel 1, though involved adolescents reported substantially lower baseline happiness (b_mod = -0.864)."},
        "p2": {"b_int":  0.161, "se": 0.169, "p_sig": "p = n.s.",    "n":  626, "r2": 0.151,
               "note": "No significant interaction in Panel 2. Wide confidence bands reflect limited precision; the bullying subgroup is small and estimates are imprecise."},
    },
}

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

ALL_LABELS = list(LABEL_TO_KEY.keys())

# ---------------------------------------------------------------------------
# Session state — track selected moderator
# ---------------------------------------------------------------------------
if "selected_mod" not in st.session_state:
    st.session_state.selected_mod = ALL_LABELS[0]

# ---------------------------------------------------------------------------
# CSS for scrapbook shape buttons
# ---------------------------------------------------------------------------
SHAPE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap');

div.mod-btn-row-1,
div.mod-btn-row-2 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 0.5rem 0;
}

div.mod-btn-row-1 .stButton > button,
div.mod-btn-row-2 .stButton > button {
    all: unset !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-family: 'Caveat', cursive !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: transform 0.15s ease, filter 0.15s ease !important;
    width: 100% !important;
    min-height: 90px !important;
    padding: 10px 8px !important;
    box-sizing: border-box !important;
    word-break: break-word !important;
    white-space: normal !important;
}

div.mod-btn-row-1 .stButton > button:hover,
div.mod-btn-row-2 .stButton > button:hover {
    transform: scale(1.07) rotate(-1.5deg) !important;
    filter: brightness(1.08) !important;
}

/* ── Row 1 shapes & colours ── */
div.mod-btn-row-1 > div:nth-child(1) .stButton > button {
    background-color: #e69c67 !important;
    color: #27304a !important;
    border-radius: 50% 50% 50% 50% / 55% 55% 45% 45% !important;
}
div.mod-btn-row-1 > div:nth-child(2) .stButton > button {
    background-color: #fdf489 !important;
    color: #27304a !important;
    border-radius: 42% 58% 44% 56% / 55% 45% 58% 42% !important;
}
div.mod-btn-row-1 > div:nth-child(3) .stButton > button {
    background-color: #2e4b62 !important;
    color: #fefdf9 !important;
    clip-path: polygon(0% 0%, 100% 0%, 88% 50%, 100% 100%, 0% 100%, 12% 50%) !important;
    border-radius: 0 !important;
}
div.mod-btn-row-1 > div:nth-child(4) .stButton > button {
    background-color: #97c58a !important;
    color: #fefdf9 !important;
    clip-path: polygon(50% 0%,55% 18%,68% 5%,63% 23%,80% 18%,68% 33%,88% 35%,72% 46%,85% 57%,67% 55%,72% 73%,55% 63%,50% 82%,45% 63%,28% 73%,33% 55%,15% 57%,28% 46%,12% 35%,32% 33%,20% 18%,37% 23%,32% 5%,45% 18%) !important;
    border-radius: 0 !important;
    min-height: 100px !important;
}

/* ── Row 2 shapes & colours ── */
div.mod-btn-row-2 > div:nth-child(1) .stButton > button {
    background-color: #ebc8bb !important;
    color: #27304a !important;
    border-radius: 50% 50% 50% 50% / 55% 55% 45% 45% !important;
}
div.mod-btn-row-2 > div:nth-child(2) .stButton > button {
    background-color: #fdf489 !important;
    color: #27304a !important;
    border-radius: 56% 44% 55% 45% / 45% 55% 42% 58% !important;
}
div.mod-btn-row-2 > div:nth-child(3) .stButton > button {
    background-color: #27304a !important;
    color: #fefdf9 !important;
    clip-path: polygon(0% 0%, 100% 0%, 88% 50%, 100% 100%, 0% 100%, 12% 50%) !important;
    border-radius: 0 !important;
}
div.mod-btn-row-2 > div:nth-child(4) .stButton > button {
    background-color: #97c58a !important;
    color: #27304a !important;
    clip-path: polygon(50% 0%,55% 18%,68% 5%,63% 23%,80% 18%,68% 33%,88% 35%,72% 46%,85% 57%,67% 55%,72% 73%,55% 63%,50% 82%,45% 63%,28% 73%,33% 55%,15% 57%,28% 46%,12% 35%,32% 33%,20% 18%,37% 23%,32% 5%,45% 18%) !important;
    border-radius: 0 !important;
    min-height: 100px !important;
}

/* ── Active / selected state — black ring ── */
div.mod-btn-row-1 > div:nth-child(1) .stButton > button[kind="secondary"],
div.mod-btn-row-1 > div:nth-child(2) .stButton > button[kind="secondary"],
div.mod-btn-row-1 > div:nth-child(3) .stButton > button[kind="secondary"],
div.mod-btn-row-1 > div:nth-child(4) .stButton > button[kind="secondary"],
div.mod-btn-row-2 > div:nth-child(1) .stButton > button[kind="secondary"],
div.mod-btn-row-2 > div:nth-child(2) .stButton > button[kind="secondary"],
div.mod-btn-row-2 > div:nth-child(3) .stButton > button[kind="secondary"],
div.mod-btn-row-2 > div:nth-child(4) .stButton > button[kind="secondary"] {
    outline: 3px solid #000 !important;
    outline-offset: 3px !important;
}
</style>
"""


def _scrapbook_buttons():
    """Render two rows of 4 scrapbook-shaped buttons. Returns selected label."""
    st.markdown(SHAPE_CSS, unsafe_allow_html=True)

    selected = st.session_state.selected_mod
    row1 = ALL_LABELS[:4]
    row2 = ALL_LABELS[4:]

    # Row 1
    st.markdown('<div class="mod-btn-row-1">', unsafe_allow_html=True)
    cols1 = st.columns(4)
    for col, label in zip(cols1, row1):
        with col:
            # Show active state via bold label prefix
            display = f"✦ {label}" if label == selected else label
            if st.button(display, key=f"mod_{label}"):
                st.session_state.selected_mod = label
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Row 2
    st.markdown('<div class="mod-btn-row-2">', unsafe_allow_html=True)
    cols2 = st.columns(4)
    for col, label in zip(cols2, row2):
        with col:
            display = f"✦ {label}" if label == selected else label
            if st.button(display, key=f"mod_{label}"):
                st.session_state.selected_mod = label
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    return st.session_state.selected_mod


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

# Render scrapbook buttons — returns currently selected label
selected_label = _scrapbook_buttons()

# Build chart with correct moderator pre-selected
mod_keys_ordered = list(LABEL_TO_KEY.keys())
selected_index   = mod_keys_ordered.index(selected_label)

fig2 = build_chart2(mod_data)

traces_per_mod = []
for key in LABEL_TO_KEY.values():
    n_groups = len(mod_data[key]["groups"])
    traces_per_mod.append(n_groups * 4)

total_traces = sum(traces_per_mod)
vis = [False] * total_traces
sl  = [False] * total_traces
offset   = sum(traces_per_mod[:selected_index])
n_traces = traces_per_mod[selected_index]
n_groups = len(mod_data[list(LABEL_TO_KEY.values())[selected_index]]["groups"])

for j in range(n_traces):
    vis[offset + j] = True
for j in range(n_groups):
    sl[offset + j * 2 + 1] = True

for i, trace in enumerate(fig2.data):
    trace.visible = vis[i]
    if hasattr(trace, "showlegend"):
        trace.showlegend = sl[i]

st.plotly_chart(style_fig(fig2), use_container_width=True)

# ---------------------------------------------------------------------------
# Dynamic caption
# ---------------------------------------------------------------------------
cap = MOD_CAPTIONS[selected_label]
p1  = cap["p1"]
p2  = cap["p2"]

st.caption(
    f"Moderator: {selected_label}. "
    f"{cap['levels']} "
    f"| Panel 1 (2010-14): interaction coefficient b = {p1['b_int']:+.3f} "
    f"(SE = {p1['se']:.3f}), {p1['p_sig']}, N = {p1['n']:,}, R\u00b2 = {p1['r2']:.3f}. "
    f"{p1['note']} "
    f"| Panel 2 (2015-19): interaction coefficient b = {p2['b_int']:+.3f} "
    f"(SE = {p2['se']:.3f}), {p2['p_sig']}, N = {p2['n']:,}, R\u00b2 = {p2['r2']:.3f}. "
    f"{p2['note']} "
    f"| Confidence bands: +/-1.96 x SE(b_int) x SM hours x moderator value. "
    f"Source: Understanding Society (UKHLS), waves 2010-2019."
)

# ---------------------------------------------------------------------------
# Export to HTML
# ---------------------------------------------------------------------------
html_bytes = style_fig(fig2).to_html(
    full_html=True,
    include_plotlyjs="cdn",   # loads Plotly from CDN — keeps file small (~1 MB vs ~3 MB)
    config={"responsive": True, "displayModeBar": True},
).encode("utf-8")

st.download_button(
    label="⬇ Download chart as HTML",
    data=html_bytes,
    file_name=f"moderator_{LABEL_TO_KEY[selected_label]}.html",
    mime="text/html",
    help="Standalone HTML file — drop it into any webpage with an <iframe> or open directly in a browser.",
)

section_rule()

# ---------------------------------------------------------------------------
# Section 3: Risk profile widget
# ---------------------------------------------------------------------------
render_widget()

app_footer()

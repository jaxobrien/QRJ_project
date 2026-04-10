import streamlit as st
from utils.data_loader import load_panels, build_moderator_data
from utils.charts.panel_overview import build_chart1
from utils.charts.moderator_toggle import build_chart2
from utils.charts.risk_profile_widget import render_widget
from style import apply_styles, style_fig, pull_quote, finding_card, section_rule, app_footer

# apply_styles() calls st.set_page_config internally — do not call it separately
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
# Page header
# ---------------------------------------------------------------------------
st.title("Social Media & Adolescent Happiness")
st.markdown(
    "How does daily social media use relate to the happiness of UK adolescents "
    "aged 10 to 15 — and who is most at risk?"
)

section_rule()  # styled dashed divider replaces st.divider()

# ---------------------------------------------------------------------------
# Section 1: Overview chart
# ---------------------------------------------------------------------------
st.subheader("Happiness falls as social media use rises")
st.markdown(
    "Across both panels, mean happiness declines steadily from age 10 to 15, "
    "while weekday social media use increases. The gap between the two cohorts "
    "widens with age, with adolescents in the 2015–2019 panel spending more time "
    "online and reporting lower happiness by age 15."
)
st.plotly_chart(
    style_fig(build_chart1(df1, df2)),  # applies palette + fonts to chart
    use_container_width=True,
)
st.caption(
    "Source: Understanding Society (UK Household Longitudinal Study), waves 2010–2019. "
    "N = 919 unique participants across both panels. Ages 10–15 only."
)

section_rule()

# ---------------------------------------------------------------------------
# Section 2: Moderator toggle
# ---------------------------------------------------------------------------
st.subheader("Who is most affected?")
st.markdown(
    "The relationship between social media use and happiness is not the same for "
    "everyone. Use the buttons below to explore how individual characteristics — "
    "sex, self-esteem, mental health, physical health, parental and sibling "
    "relationships, leisure activity, and bullying — shape that relationship. "
    "Lines show mean observed happiness at each level of social media use. "
    "Data shown separately for each panel cohort."
)
st.plotly_chart(
    style_fig(build_chart2(mod_data)),  # applies palette + fonts to chart
    use_container_width=True,
)
st.caption(
    "Mean observed happiness by social media hours. Health shown at all five "
    "survey levels. Index variables (self-esteem, parental relationship, sibling "
    "relationship, leisure) shown at integer scale levels using observations within "
    "±0.5 of each level. SDQ uses clinical bands: Normal (0–15), Borderline (16–19), "
    "Abnormal (20–40) — borderline and abnormal groups are small; interpret with "
    "caution. Bullying: involved if any bullying variable equals 1. "
    "Self-esteem level 1 excluded (n=4). Leisure level 4 incomplete at high SM hours."
)

section_rule()

# ---------------------------------------------------------------------------
# Section 3: Risk profile widget
# ---------------------------------------------------------------------------
render_widget()

app_footer()  # source line at the bottom

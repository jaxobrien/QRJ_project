import streamlit as st
from utils.data_loader import load_panels, moderator_groups
from utils.charts.panel_overview import build_chart1
from utils.charts.moderator_toggle import build_chart2
from utils.charts.risk_profile_widget import render_widget

st.set_page_config(
    page_title="Social Media & Adolescent Happiness",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Load data once and cache
# ---------------------------------------------------------------------------
@st.cache_data
def get_data():
    return load_panels()

df1, df2, df_combined = get_data()

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title("Social Media & Adolescent Happiness")
st.markdown(
    "How does daily social media use relate to the happiness of UK adolescents "
    "aged 10 to 15 — and who is most at risk?"
)

st.divider()

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
st.plotly_chart(build_chart1(df1, df2), use_container_width=True)
st.caption(
    "Source: Understanding Society (UK Household Longitudinal Study), waves 2010–2019. "
    "N = 919 unique participants across both panels. Ages 10–15 only."
)

st.divider()

# ---------------------------------------------------------------------------
# Section 2: Moderator toggle
# ---------------------------------------------------------------------------
st.subheader("Who is most affected?")
st.markdown(
    "The relationship between social media use and happiness is not the same for "
    "everyone. Use the buttons to explore how individual characteristics — "
    "self-esteem, mental health, parental support, physical health, and sex — "
    "shape the happiness trajectories of adolescents as they age. "
    "Groups are defined as approximately one standard deviation above and below "
    "the sample mean."
)
st.plotly_chart(build_chart2(df_combined), use_container_width=True)
st.caption(
    "Groups represent approximately ±1 SD from the sample mean on each measure. "
    "Sex is shown as a binary split. Data pooled across both panels."
)

st.divider()

# ---------------------------------------------------------------------------
# Section 3: Risk profile widget
# ---------------------------------------------------------------------------
render_widget()

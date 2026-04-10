"""
style.py
--------
Central styling module for the Social Media & Adolescent Happiness scrollytelling app.
Import and call apply_styles() at the top of every Streamlit page/app file.

Palette (from Styleguide):
  Space Indigo   #27304a  — primary text, dark headings
  Charcoal Blue  #2e4b62  — accent, links, buttons
  Willow Green   #97c58a  — positive/highlight
  Banana Cream   #fdf489  — callout backgrounds
  Toasted Almond #e69c67  — warm accent, chart elements
  Almond Silk    #ebc8bb  — soft backgrounds, cards
  Lemon Chiffon  #faf5cc  — sidebar / secondary bg
  Porcelain      #fefdf9  — main background

Fonts (loaded via Google Fonts):
  Caveat    — display / pull-quotes / handwritten flavour
  Lora      — section headings (editorial serif)
  DM Sans   — body / UI text
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# ── Colour tokens ──────────────────────────────────────────────────────────────
PALETTE = {
    "black":          "#000000",
    "space_indigo":   "#27304a",
    "charcoal_blue":  "#2e4b62",
    "willow_green":   "#97c58a",
    "banana_cream":   "#fdf489",
    "toasted_almond": "#e69c67",
    "almond_silk":    "#ebc8bb",
    "lemon_chiffon":  "#faf5cc",
    "porcelain":      "#fefdf9",
}

# Chart line/group colours — drawn from the palette for consistency
CHART_COLORS = [
    "#2e4b62",   # Charcoal Blue
    "#e69c67",   # Toasted Almond
    "#97c58a",   # Willow Green
    "#fdf489",   # Banana Cream (use on dark backgrounds only)
    "#27304a",   # Space Indigo
    "#ebc8bb",   # Almond Silk
]


# ── Plotly theme ───────────────────────────────────────────────────────────────
def register_plotly_theme():
    """Register a custom Plotly template called 'wellbeing'."""
    pio.templates["wellbeing"] = go.layout.Template(
        layout=go.Layout(
            font=dict(family="DM Sans, sans-serif", color=PALETTE["space_indigo"], size=13),
            title=dict(
                font=dict(family="Lora, serif", size=20, color=PALETTE["space_indigo"]),
                x=0.0,
                xanchor="left",
            ),
            paper_bgcolor=PALETTE["porcelain"],
            plot_bgcolor="#ffffff",
            colorway=CHART_COLORS,
            xaxis=dict(
                gridcolor="#eeeeee",
                linecolor=PALETTE["almond_silk"],
                tickfont=dict(family="DM Sans, sans-serif", size=12),
                title_font=dict(family="DM Sans, sans-serif", size=13),
            ),
            yaxis=dict(
                gridcolor="#eeeeee",
                linecolor=PALETTE["almond_silk"],
                tickfont=dict(family="DM Sans, sans-serif", size=12),
                title_font=dict(family="DM Sans, sans-serif", size=13),
            ),
            legend=dict(
                bgcolor="rgba(254,253,249,0.9)",
                bordercolor=PALETTE["almond_silk"],
                borderwidth=1,
                font=dict(family="DM Sans, sans-serif", size=12),
            ),
            margin=dict(t=60, b=60, l=60, r=30),
            hoverlabel=dict(
                bgcolor=PALETTE["lemon_chiffon"],
                bordercolor=PALETTE["toasted_almond"],
                font=dict(family="DM Sans, sans-serif", size=12, color=PALETTE["space_indigo"]),
            ),
            annotations=[],
        )
    )
    pio.templates.default = "wellbeing"


# ── CSS injection ──────────────────────────────────────────────────────────────
_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

/* ── Root tokens ── */
:root {
    --col-black:          #000000;
    --col-indigo:         #27304a;
    --col-blue:           #2e4b62;
    --col-green:          #97c58a;
    --col-yellow:         #fdf489;
    --col-almond:         #e69c67;
    --col-silk:           #ebc8bb;
    --col-chiffon:        #faf5cc;
    --col-porcelain:      #fefdf9;
    --font-display:       'Caveat', cursive;
    --font-heading:       'Lora', serif;
    --font-body:          'DM Sans', sans-serif;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    color: var(--col-indigo);
    background-color: var(--col-porcelain);
}

/* ── Main container ── */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 860px;
}

/* ── Headings ── */
h1 {
    font-family: var(--font-display) !important;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    color: var(--col-indigo) !important;
    line-height: 1.15 !important;
    margin-bottom: 0.25rem !important;
}

h2 {
    font-family: var(--font-heading) !important;
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    color: var(--col-blue) !important;
    margin-top: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    border-bottom: 2px solid var(--col-chiffon);
    padding-bottom: 0.3rem;
}

h3 {
    font-family: var(--font-heading) !important;
    font-size: 1.25rem !important;
    font-weight: 400 !important;
    font-style: italic !important;
    color: var(--col-blue) !important;
    margin-top: 1.5rem !important;
}

/* ── Body text ── */
p, li, label {
    font-family: var(--font-body) !important;
    font-size: 1.02rem !important;
    line-height: 1.75 !important;
    color: var(--col-indigo);
}

/* ── Pull-quote / Caveat callout ── */
.pull-quote {
    font-family: var(--font-display) !important;
    font-size: 1.9rem;
    color: var(--col-blue);
    border-left: 4px solid var(--col-almond);
    padding: 0.6rem 1.2rem;
    margin: 1.8rem 0;
    background: var(--col-chiffon);
    border-radius: 0 8px 8px 0;
}

/* ── Stat callout box ── */
.stat-box {
    background: var(--col-yellow);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    border: 1.5px solid var(--col-almond);
}
.stat-box .stat-number {
    font-family: var(--font-display);
    font-size: 3rem;
    font-weight: 700;
    color: var(--col-blue);
    display: block;
    line-height: 1;
}
.stat-box .stat-label {
    font-family: var(--font-body);
    font-size: 0.85rem;
    color: var(--col-indigo);
    margin-top: 0.3rem;
    display: block;
}

/* ── Info / finding card ── */
.finding-card {
    background: var(--col-silk);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 1rem 0;
    border-left: 4px solid var(--col-blue);
}
.finding-card p { margin: 0; }

/* ── Section divider ── */
.section-rule {
    border: none;
    border-top: 2px dashed var(--col-almond);
    margin: 2.5rem 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--col-chiffon) !important;
    border-right: 1.5px solid var(--col-silk);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--col-indigo) !important;
    font-family: var(--font-heading) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: var(--col-indigo) !important;
}

/* ── Streamlit widgets ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] label,
div[data-testid="stSlider"] label {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    color: var(--col-blue) !important;
}

/* Selectbox / dropdown border */
div[data-baseweb="select"] > div {
    border-color: var(--col-blue) !important;
    background-color: var(--col-porcelain) !important;
}

/* Buttons */
.stButton > button {
    font-family: var(--font-body) !important;
    font-weight: 500;
    background-color: var(--col-blue) !important;
    color: var(--col-porcelain) !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.45rem 1.2rem !important;
    transition: background 0.2s ease;
}
.stButton > button:hover {
    background-color: var(--col-indigo) !important;
}

/* Radio buttons */
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: var(--col-chiffon);
    border: 1.5px solid var(--col-silk);
    border-radius: 6px;
    padding: 0.3rem 0.8rem;
    margin-right: 0.4rem;
    transition: background 0.15s;
    cursor: pointer;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background: var(--col-yellow);
}

/* Slider thumb colour */
div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--col-blue) !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: var(--col-chiffon);
    border: 1.5px solid var(--col-silk);
    border-radius: 10px;
    padding: 0.8rem 1rem !important;
}
div[data-testid="metric-container"] label {
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
    color: var(--col-blue) !important;
    font-weight: 500 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 2.2rem !important;
    color: var(--col-indigo) !important;
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    color: var(--col-blue) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom-color: var(--col-almond) !important;
    color: var(--col-indigo) !important;
}

/* ── Expander ── */
details summary {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    color: var(--col-blue) !important;
}

/* ── Scrollytelling hero section ── */
.hero-section {
    background: linear-gradient(135deg, var(--col-chiffon) 0%, var(--col-silk) 100%);
    border-radius: 14px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    border: 1.5px solid var(--col-almond);
}
.hero-section h1 {
    font-size: 3.8rem !important;
    margin-bottom: 1rem !important;
}
.hero-section .subtitle {
    font-family: var(--font-heading);
    font-style: italic;
    font-size: 1.15rem;
    color: var(--col-blue);
    line-height: 1.6;
}

/* ── Scroll section marker ── */
.scroll-marker {
    text-align: center;
    font-family: var(--font-display);
    font-size: 1.1rem;
    color: var(--col-almond);
    margin: 1rem 0 0.5rem 0;
    letter-spacing: 0.05em;
}

/* ── Annotation badge (for chart callouts) ── */
.chart-badge {
    display: inline-block;
    background: var(--col-yellow);
    color: var(--col-indigo);
    font-family: var(--font-body);
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
    border: 1px solid var(--col-almond);
    margin-right: 0.3rem;
}

/* ── Footer ── */
.app-footer {
    font-family: var(--font-body);
    font-size: 0.8rem;
    color: var(--col-blue);
    text-align: center;
    border-top: 1px solid var(--col-silk);
    padding-top: 1.2rem;
    margin-top: 4rem;
    opacity: 0.75;
}
</style>
"""


# ── Helper components (render via st.markdown) ─────────────────────────────────

def pull_quote(text: str) -> None:
    """Render a Caveat-font pull quote."""
    st.markdown(f'<div class="pull-quote">{text}</div>', unsafe_allow_html=True)


def stat_box(number: str, label: str) -> None:
    """Render a highlighted stat box."""
    st.markdown(
        f"""<div class="stat-box">
            <span class="stat-number">{number}</span>
            <span class="stat-label">{label}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def finding_card(text: str) -> None:
    """Render a coloured finding / insight card."""
    st.markdown(f'<div class="finding-card"><p>{text}</p></div>', unsafe_allow_html=True)


def section_rule() -> None:
    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    """Render the opening hero block."""
    st.markdown(
        f"""<div class="hero-section">
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
        </div>""",
        unsafe_allow_html=True,
    )


def app_footer(source: str = "Source: Understanding Society (UKHLS), Waves 2–9") -> None:
    st.markdown(f'<div class="app-footer">{source}</div>', unsafe_allow_html=True)


# ── Plotly figure post-processor ───────────────────────────────────────────────

def style_fig(fig: go.Figure, title: str = "", subtitle: str = "") -> go.Figure:
    """
    Apply wellbeing theme overrides to any Plotly figure.
    Call this after building your figure in moderator_toggle.py or elsewhere.

    Usage:
        fig = build_chart2(mod_data)
        fig = style_fig(fig, title="Social media hours & happiness")
        st.plotly_chart(fig, use_container_width=True)
    """
    full_title = f"<b>{title}</b><br><span style='font-size:13px;color:{PALETTE[\"charcoal_blue\"]};font-style:italic'>{subtitle}</span>" if subtitle else f"<b>{title}</b>"

    fig.update_layout(
        template="wellbeing",
        title_text=full_title if title else "",
        paper_bgcolor=PALETTE["porcelain"],
        plot_bgcolor="#ffffff",
        font=dict(family="DM Sans, sans-serif", color=PALETTE["space_indigo"], size=13),
        legend=dict(
            bgcolor="rgba(254,253,249,0.92)",
            bordercolor=PALETTE["almond_silk"],
            borderwidth=1,
            font=dict(family="DM Sans, sans-serif", size=12),
        ),
        hoverlabel=dict(
            bgcolor=PALETTE["lemon_chiffon"],
            bordercolor=PALETTE["toasted_almond"],
            font=dict(family="DM Sans, sans-serif", size=12, color=PALETTE["space_indigo"]),
        ),
        # Subplot panel titles → Lora italic
        annotations=[
            ann.update(font=dict(family="Lora, serif", size=15, color=PALETTE["charcoal_blue"])) or ann
            for ann in fig.layout.annotations
        ],
    )

    # Restyle all axes
    for axis_name in [k for k in fig.layout._props if k.startswith(("xaxis", "yaxis"))]:
        axis = getattr(fig.layout, axis_name)
        axis.update(
            gridcolor="#eeeeee",
            linecolor=PALETTE["almond_silk"],
            tickfont=dict(family="DM Sans, sans-serif", size=11),
            title_font=dict(family="DM Sans, sans-serif", size=12, color=PALETTE["charcoal_blue"]),
        )

    # Restyle toggle buttons (updatemenus)
    for menu in fig.layout.updatemenus:
        menu.update(
            bgcolor=PALETTE["lemon_chiffon"],
            bordercolor=PALETTE["almond_silk"],
            font=dict(family="DM Sans, sans-serif", size=12, color=PALETTE["space_indigo"]),
            active=0,
        )

    return fig


# ── Main entry point ───────────────────────────────────────────────────────────

def apply_styles() -> None:
    """
    Call once at the top of your Streamlit app:

        from style import apply_styles
        apply_styles()
    """
    st.set_page_config(
        page_title="Social Media & Adolescent Happiness",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    register_plotly_theme()
    st.markdown(_CSS, unsafe_allow_html=True)

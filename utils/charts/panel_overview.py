import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import means_by_age

AGES = list(range(10, 16))

PANEL_COLOURS = {
    "2010–2014": "#4C9BE8",  # blue
    "2015–2019": "#E8714C",  # orange-red
}

ONLINE_HRS_LABELS = {
    0: "None",
    1: "<1 hour",
    2: "1–3 hours",
    3: "4–6 hours",
    4: "7+ hours",
}


def build_chart1(df1, df2):
    """
    Side-by-side line charts replicating the ggplot style:
    Left:  mean happiness by age, Panel 1 vs Panel 2
    Right: mean social media hours by age, Panel 1 vs Panel 2
    """
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Happiness", "Social media use"),
        horizontal_spacing=0.12,
    )

    datasets = [
        (df1, "2010–2014"),
        (df2, "2015–2019"),
    ]

    for df, panel_label in datasets:
        colour = PANEL_COLOURS[panel_label]
        show_legend = True

        # --- Left: happiness ---
        hap = means_by_age(df, "happiness_index")
        fig.add_trace(
            go.Scatter(
                x=AGES,
                y=[hap.get(a) for a in AGES],
                mode="lines+markers",
                name=panel_label,
                line=dict(color=colour, width=2),
                marker=dict(size=6, color=colour),
                legendgroup=panel_label,
                showlegend=show_legend,
            ),
            row=1, col=1,
        )

        # --- Right: online_hrs ---
        sm = means_by_age(df, "online_hrs")
        fig.add_trace(
            go.Scatter(
                x=AGES,
                y=[sm.get(a) for a in AGES],
                mode="lines+markers",
                name=panel_label,
                line=dict(color=colour, width=2),
                marker=dict(size=6, color=colour),
                legendgroup=panel_label,
                showlegend=False,  # already in legend from left panel
            ),
            row=1, col=2,
        )

    # --- Y-axis: happiness (1-7 scale with survey labels) ---
    fig.update_yaxes(
        title_text="Mean happiness",
        range=[1, 7],
        tickvals=[1, 2, 3, 4, 5, 6, 7],
        ticktext=[
            "Not at all<br>happy", "2", "3", "4", "5", "6", "Completely<br>happy"
        ],
        row=1, col=1,
    )

    # --- Y-axis: online_hrs (0-4 ordinal with survey labels) ---
    fig.update_yaxes(
        title_text="Weekday social media use",
        range=[0, 4],
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["None", "<1 hour", "1–3 hours", "4–6 hours", "7+ hours"],
        row=1, col=2,
    )

    # --- Shared x-axis formatting ---
    for col in [1, 2]:
        fig.update_xaxes(
            title_text="Age",
            tickvals=AGES,
            row=1, col=col,
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            title_text="Panel",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=60, b=80, l=60, r=30),
        height=420,
    )

    fig.update_xaxes(showgrid=True, gridcolor="#EEEEEE")
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE")

    return fig

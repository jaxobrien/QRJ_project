import plotly.graph_objects as go
from utils.data_loader import moderator_groups

AGES = list(range(10, 16))

# Colours for low/high groups
LOW_COLOUR = "#E8714C"   # orange-red = more vulnerable group
HIGH_COLOUR = "#4C9BE8"  # blue = more resilient group

# Note: for SDQ, higher score = more difficulties = worse outcome,
# so "high" SDQ is the vulnerable group. Labels handle this in data_loader.


def build_chart2(df_combined):
    """
    Single line chart with toggle buttons for each moderator.
    Shows mean happiness by age for -1SD group and +1SD group (or binary split).
    One set of traces per moderator; only the active moderator is visible.
    """
    mods = moderator_groups(df_combined)
    mod_keys = list(mods.keys())

    fig = go.Figure()

    # Build one pair of traces per moderator
    for i, key in enumerate(mod_keys):
        m = mods[key]
        visible = (i == 0)  # only first moderator visible initially

        # Low group
        fig.add_trace(go.Scatter(
            x=AGES,
            y=list(m["low"]),
            mode="lines+markers",
            name=m["low_label"],
            line=dict(color=LOW_COLOUR, width=2, dash="dash"),
            marker=dict(size=6, color=LOW_COLOUR),
            visible=visible,
            legendgroup="low",
            showlegend=visible,
        ))

        # High group
        fig.add_trace(go.Scatter(
            x=AGES,
            y=list(m["high"]),
            mode="lines+markers",
            name=m["high_label"],
            line=dict(color=HIGH_COLOUR, width=2),
            marker=dict(size=6, color=HIGH_COLOUR),
            visible=visible,
            legendgroup="high",
            showlegend=visible,
        ))

    # Build toggle buttons — each button shows only its 2 traces
    buttons = []
    for i, key in enumerate(mod_keys):
        m = mods[key]
        n_traces = len(mod_keys) * 2
        visibility = [False] * n_traces
        visibility[i * 2] = True      # low trace
        visibility[i * 2 + 1] = True  # high trace

        # Update legend labels dynamically via trace updates
        buttons.append(dict(
            label=m["label"],
            method="update",
            args=[
                {
                    "visible": visibility,
                    "name": [m["low_label"] if j == i * 2 else
                             m["high_label"] if j == i * 2 + 1 else
                             "" for j in range(n_traces)],
                },
                {
                    "legend.title.text": m["label"],
                },
            ],
        ))

    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            direction="right",
            x=0.5,
            xanchor="center",
            y=1.18,
            yanchor="top",
            buttons=buttons,
            showactive=True,
            bgcolor="#F0F0F0",
            bordercolor="#CCCCCC",
            font=dict(size=12),
        )],
        yaxis=dict(
            title="Mean happiness",
            range=[3.5, 7],
            tickvals=[4, 5, 6, 7],
            ticktext=["4", "5", "6", "Completely<br>happy (7)"],
            showgrid=True,
            gridcolor="#EEEEEE",
        ),
        xaxis=dict(
            title="Age",
            tickvals=AGES,
            showgrid=True,
            gridcolor="#EEEEEE",
        ),
        legend=dict(
            title_text=mods[mod_keys[0]]["label"],
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=80, b=90, l=60, r=30),
        height=460,
    )

    return fig

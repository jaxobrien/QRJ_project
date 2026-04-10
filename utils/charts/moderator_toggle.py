import plotly.graph_objects as go
from plotly.subplots import make_subplots

SM_TICK_VALS  = [0, 1, 2, 3, 4]
SM_TICK_TEXT  = ["None", "<1 hr", "1–3 hrs", "4–6 hrs", "7+ hrs"]
X_VALS        = SM_TICK_VALS


def build_chart2(mod_data):
    """
    Toggle chart: mean observed happiness by social media hours,
    split by moderator group, side-by-side Panel 1 / Panel 2.

    mod_data: output of build_moderator_data() from data_loader.
    """
    mod_keys = list(mod_data.keys())
    traces_per_mod = []

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Panel 1 (2010–2014)", "Panel 2 (2015–2019)"),
        horizontal_spacing=0.10,
    )

    for i, key in enumerate(mod_keys):
        mod     = mod_data[key]
        visible = (i == 0)
        n_traces = len(mod["groups"]) * 2   # × 2 panels
        traces_per_mod.append(n_traces)

        for panel_idx, panel_key in enumerate(["p1", "p2"]):
            col_num     = panel_idx + 1
            show_legend = (panel_idx == 0)

            for grp in mod["groups"]:
                y_vals = grp[panel_key]

                fig.add_trace(
                    go.Scatter(
                        x=X_VALS,
                        y=y_vals,
                        mode="lines+markers",
                        name=grp["name"],
                        line=dict(color=grp["colour"], width=2.5),
                        marker=dict(size=5, color=grp["colour"]),
                        visible=visible,
                        legendgroup=grp["name"],
                        showlegend=show_legend,
                    ),
                    row=1, col=col_num,
                )

    # ------------------------------------------------------------------
    # Toggle buttons
    # ------------------------------------------------------------------
    total_traces = sum(traces_per_mod)
    buttons      = []
    offset       = 0

    for i, key in enumerate(mod_keys):
        mod = mod_data[key]
        n   = traces_per_mod[i]

        vis = [False] * total_traces
        for j in range(n):
            vis[offset + j] = True

        buttons.append(dict(
            label=mod["label"],
            method="update",
            args=[
                {"visible": vis},
                {"legend.title.text": mod["label"]},
            ],
        ))
        offset += n

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            direction="right",
            x=0.5,
            xanchor="center",
            y=1.22,
            yanchor="top",
            buttons=buttons,
            showactive=True,
            bgcolor="#F0F0F0",
            bordercolor="#CCCCCC",
            font=dict(size=11),
        )],
        legend=dict(
            title_text=mod_data[mod_keys[0]]["label"],
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=100, b=100, l=60, r=30),
        height=500,
    )

    for col in [1, 2]:
        fig.update_xaxes(
            title_text="Social media hours (weekdays)",
            tickvals=SM_TICK_VALS,
            ticktext=SM_TICK_TEXT,
            showgrid=True,
            gridcolor="#EEEEEE",
            row=1, col=col,
        )
        fig.update_yaxes(
            title_text="Predicted happiness" if col == 1 else "",
            range=[1, 7],
            tickvals=[1, 2, 3, 4, 5, 6, 7],
            ticktext=[
                "1 — Not at all happy", "2", "3", "4", "5", "6", "7 — Completely happy"
            ],
            showgrid=True,
            gridcolor="#EEEEEE",
            row=1, col=col,
        )

    return fig

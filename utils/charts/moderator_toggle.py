import plotly.graph_objects as go
from plotly.subplots import make_subplots

SM_TICK_VALS = [0, 1, 2, 3, 4]
SM_TICK_TEXT = ["None", "<1 hr", "1–3 hrs", "4–6 hrs", "7+ hrs"]
X_VALS       = SM_TICK_VALS


def build_chart2(mod_data):
    mod_keys = list(mod_data.keys())
    traces_per_mod = []

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Panel 1 (2010–2014)", "Panel 2 (2015–2019)"),
        horizontal_spacing=0.10,
    )

    # ------------------------------------------------------------------
    # Add ALL traces — only first moderator visible at load.
    # showlegend=True only for panel 1 traces of the first moderator.
    # All others start with showlegend=False and are updated by buttons.
    # ------------------------------------------------------------------
    for i, key in enumerate(mod_keys):
        mod     = mod_data[key]
        visible = (i == 0)

        n_traces = len(mod["groups"]) * 2
        traces_per_mod.append(n_traces)

        for panel_idx, panel_key in enumerate(["p1", "p2"]):
            col_num     = panel_idx + 1
            # Only the first moderator, first panel gets showlegend=True at load
            show_legend = (i == 0 and panel_idx == 0)

            for grp in mod["groups"]:
                fig.add_trace(
                    go.Scatter(
                        x=X_VALS,
                        y=grp[panel_key],
                        mode="lines+markers",
                        name=grp["name"],
                        line=dict(color=grp["colour"], width=2.5),
                        marker=dict(size=5, color=grp["colour"]),
                        visible=visible,
                        legendgroup=f"{key}::{grp['name']}",
                        showlegend=show_legend,
                    ),
                    row=1, col=col_num,
                )

    # ------------------------------------------------------------------
    # Build button args — each button sets visible AND showlegend
    # so only the active moderator's panel-1 traces appear in legend
    # ------------------------------------------------------------------
    total_traces = sum(traces_per_mod)

    # Pre-compute per-trace whether it is a panel-1 trace
    # Panel 1 traces are added first within each moderator block
    # Order per moderator: [p1_grp0, p1_grp1, ..., p2_grp0, p2_grp1, ...]
    buttons = []
    offset  = 0

    for i, key in enumerate(mod_keys):
        mod        = mod_data[key]
        n_groups   = len(mod["groups"])
        n          = traces_per_mod[i]

        vis          = [False] * total_traces
        show_legend  = [False] * total_traces

        for j in range(n):
            vis[offset + j] = True
            # Panel 1 traces are the first n_groups within this moderator's block
            if j < n_groups:
                show_legend[offset + j] = True

        buttons.append(dict(
            label=mod["label"],
            method="update",
            args=[
                {
                    "visible":    vis,
                    "showlegend": show_legend,
                },
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
            font=dict(size=12),
        )],
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=-0.30,
            xanchor="center",
            x=0.5,
            font=dict(size=13),
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(t=110, b=110, l=70, r=30),
        height=520,
    )

    # Subplot titles are annotations — increase font size
    for annotation in fig.layout.annotations:
        annotation.update(font=dict(size=16, family="Arial, sans-serif"))

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
            ticktext=["1 — Not at all happy", "2", "3", "4", "5", "6", "7 — Completely happy"],
            showgrid=True,
            gridcolor="#EEEEEE",
            row=1, col=col,
        )

    return fig

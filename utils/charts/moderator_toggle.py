import plotly.graph_objects as go
from plotly.subplots import make_subplots

SM_TICK_VALS = [0, 1, 2, 3, 4]
SM_TICK_TEXT = ["None", "<1 hr", "1–3 hrs", "4–6 hrs", "7+ hrs"]
X_VALS       = SM_TICK_VALS


def _hex_to_rgba(hex_colour, alpha=0.15):
    """Convert hex colour to rgba string for shaded bands."""
    h = hex_colour.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def build_chart2(mod_data):
    mod_keys = list(mod_data.keys())
    traces_per_mod = []

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Panel 1 (2010–2014)", "Panel 2 (2015–2019)"),
        horizontal_spacing=0.10,
    )

    # ------------------------------------------------------------------
    # Add traces — for each group: CI band (filled) then line on top.
    # Band uses upper+lower values joined into a single filled polygon.
    # Only first moderator visible at load; showlegend only for p1 traces.
    # ------------------------------------------------------------------
    for i, key in enumerate(mod_keys):
        mod      = mod_data[key]
        visible  = (i == 0)
        n_groups = len(mod["groups"])
        # 2 traces per group per panel (band + line) × 2 panels = 4 per group
        n_traces = n_groups * 4
        traces_per_mod.append(n_traces)

        for panel_idx, panel_key in enumerate(["p1", "p2"]):
            col_num     = panel_idx + 1
            show_legend = (i == 0 and panel_idx == 0)

            for grp in mod["groups"]:
                upper = grp[f"{panel_key}_upper"]
                lower = grp[f"{panel_key}_lower"]
                mid   = grp[panel_key]
                rgba  = _hex_to_rgba(grp["colour"], alpha=0.15)

                # --- CI band (filled polygon, no legend entry) ---
                fig.add_trace(
                    go.Scatter(
                        x=X_VALS + X_VALS[::-1],
                        y=upper + lower[::-1],
                        fill="toself",
                        fillcolor=rgba,
                        line=dict(color="rgba(0,0,0,0)"),
                        hoverinfo="skip",
                        showlegend=False,
                        visible=visible,
                        legendgroup=f"{key}::{grp['name']}",
                    ),
                    row=1, col=col_num,
                )

                # --- Predicted line ---
                fig.add_trace(
                    go.Scatter(
                        x=X_VALS,
                        y=mid,
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
    # Toggle buttons — update visible and showlegend together
    # ------------------------------------------------------------------
    total_traces = sum(traces_per_mod)
    buttons      = []
    offset       = 0

    for i, key in enumerate(mod_keys):
        mod      = mod_data[key]
        n_groups = len(mod["groups"])
        n        = traces_per_mod[i]

        vis = [False] * total_traces
        sl  = [False] * total_traces

        for j in range(n):
            vis[offset + j] = True

        # showlegend=True only for the line traces (odd indices within
        # each panel block) of panel 1 (first n_groups*2 traces)
        # Trace order within each moderator block:
        # [p1_grp0_band, p1_grp0_line, p1_grp1_band, p1_grp1_line, ...,
        #  p2_grp0_band, p2_grp0_line, ...]
        for j in range(n_groups):
            line_idx = offset + j * 2 + 1   # p1 line traces
            sl[line_idx] = True

        buttons.append(dict(
            label=mod["label"],
            method="update",
            args=[{"visible": vis, "showlegend": sl}],
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

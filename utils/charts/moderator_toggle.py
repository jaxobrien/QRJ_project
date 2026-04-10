import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------
# Regression coefficients from Appendix 2, Panel 1 and Panel 2 columns.
# ---------------------------------------------------------------------------
MODERATOR_CONFIGS = {
    "self_esteem": {
        "label": "Self-esteem",
        "col": "selfesteem_index",
        "low_label": "Low self-esteem (−1 SD)",
        "high_label": "High self-esteem (+1 SD)",
        "p1": {"intercept": 2.615, "b_x": -0.308, "b_mod": 1.026, "b_int": 0.089},
        "p2": {"intercept": 2.645, "b_x": -0.578, "b_mod": 1.021, "b_int": 0.157},
    },
    "sdq": {
        "label": "Mental health difficulties",
        "col": "sdq_total",
        "low_label": "Fewer difficulties (−1 SD)",
        "high_label": "More difficulties (+1 SD)",
        "p1": {"intercept": 6.705, "b_x": -0.006, "b_mod": -0.072, "b_int": -0.010},
        "p2": {"intercept": 6.974, "b_x": -0.119, "b_mod": -0.098, "b_int":  0.000},
    },
    "health": {
        "label": "Physical health",
        "col": "health",
        "low_label": "Poorer health (−1 SD)",
        "high_label": "Better health (+1 SD)",
        "p1": {"intercept": 5.046, "b_x": -0.403, "b_mod": 0.239, "b_int": 0.077},
        "p2": {"intercept": 4.772, "b_x": -0.550, "b_mod": 0.301, "b_int": 0.097},
    },
    "parent": {
        "label": "Parental support",
        "col": "parent_index",
        "low_label": "Lower parental support (−1 SD)",
        "high_label": "Higher parental support (+1 SD)",
        "p1": {"intercept": 5.659, "b_x": -0.209, "b_mod": 0.127, "b_int": 0.011},
        "p2": {"intercept": 5.811, "b_x": -0.390, "b_mod": 0.054, "b_int": 0.062},
    },
    "siblings": {
        "label": "Sibling relationships",
        "col": "sib_index",
        "low_label": "Lower sibling quality (−1 SD)",
        "high_label": "Higher sibling quality (+1 SD)",
        "p1": {"intercept": 5.212, "b_x": -0.236, "b_mod": 0.260, "b_int":  0.013},
        "p2": {"intercept": 3.693, "b_x":  0.471, "b_mod": 0.700, "b_int": -0.191},
    },
    "leisure": {
        "label": "Leisure activity",
        "col": "leisure_index",
        "low_label": "Less leisure activity (−1 SD)",
        "high_label": "More leisure activity (+1 SD)",
        "p1": {"intercept": 5.692, "b_x": -0.057, "b_mod": 0.169, "b_int": -0.043},
        "p2": {"intercept": 5.846, "b_x": -0.387, "b_mod": 0.124, "b_int":  0.095},
    },
    "drinking": {
        "label": "Alcohol use",
        "col": "drink_freq",
        "low_label": "Lower alcohol use (−1 SD)",
        "high_label": "Higher alcohol use (+1 SD)",
        "p1": {"intercept": 6.001, "b_x": -0.124, "b_mod": -0.091, "b_int": -0.051},
        "p2": {"intercept": 6.050, "b_x": -0.250, "b_mod": -0.157, "b_int":  0.000},
    },
    "tv_hours": {
        "label": "TV hours",
        "col": "tvhrs_index",
        "low_label": "Fewer TV hours (−1 SD)",
        "high_label": "More TV hours (+1 SD)",
        "p1": {"intercept": 6.106, "b_x": -0.188, "b_mod": -0.033, "b_int":  0.001},
        "p2": {"intercept": 6.275, "b_x": -0.236, "b_mod": -0.141, "b_int":  0.008},
    },
    "bullying": {
        "label": "Bullying involvement",
        "col": "bullying_mean",
        "low_label": "Lower bullying involvement (−1 SD)",
        "high_label": "Higher bullying involvement (+1 SD)",
        "p1": {"intercept": 6.216, "b_x": -0.189, "b_mod": -0.864, "b_int": -0.128},
        "p2": {"intercept": 6.220, "b_x": -0.197, "b_mod": -1.637, "b_int":  0.161},
    },
    "sex": {
        "label": "Sex",
        "col": "sex",
        "is_binary": True,
        "low_label": "Male",
        "high_label": "Female",
        "p1": {"intercept": 6.002, "b_x": -0.124, "b_mod": 0.050, "b_int": -0.095},
        "p2": {"intercept": 5.895, "b_x": -0.171, "b_mod": 0.235, "b_int": -0.121},
    },
}

COLOURS = {
    "low":  "#E8714C",
    "mean": "#4CAF50",
    "high": "#4C9BE8",
}

X_VALS = np.linspace(0, 4, 100)
X_TICK_VALS = [0, 1, 2, 3, 4]
X_TICK_TEXT = ["None", "<1 hr", "1–3 hrs", "4–6 hrs", "7+ hrs"]


def _predicted(coefs, x, mod_val):
    return (
        coefs["intercept"]
        + coefs["b_x"] * x
        + coefs["b_mod"] * mod_val
        + coefs["b_int"] * x * mod_val
    )


def _mod_stats(df_combined, col):
    if col == "bullying_mean":
        bully_cols = ["bullied_other_bin", "bullied_phys_bin", "bully_other_bin", "bully_phys_bin"]
        vals = df_combined[bully_cols].mean(axis=1)
    else:
        vals = df_combined[col].dropna()
    return vals.mean(), vals.std()


def build_chart2(df_combined):
    mod_keys = list(MODERATOR_CONFIGS.keys())
    traces_per_mod = []

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Panel 1 (2010–2014)", "Panel 2 (2015–2019)"),
        horizontal_spacing=0.10,
    )

    for i, key in enumerate(mod_keys):
        cfg = MODERATOR_CONFIGS[key]
        is_binary = cfg.get("is_binary", False)
        visible = (i == 0)

        m, s = _mod_stats(df_combined, cfg["col"])

        if is_binary:
            groups = [
                ("low",  cfg["low_label"],  0),
                ("high", cfg["high_label"], 1),
            ]
            n_traces = 4
        else:
            groups = [
                ("low",  cfg["low_label"],  m - s),
                ("mean", "Mean",             m),
                ("high", cfg["high_label"], m + s),
            ]
            n_traces = 6

        traces_per_mod.append(n_traces)

        for panel_idx, panel_key in enumerate(["p1", "p2"]):
            coefs = cfg[panel_key]
            col_num = panel_idx + 1
            show_legend = (panel_idx == 0)

            for grp_key, grp_label, mod_val in groups:
                y_vals = np.clip(_predicted(coefs, X_VALS, mod_val), 1, 7)
                dash = "dash" if grp_key == "low" else ("dot" if grp_key == "mean" else "solid")

                fig.add_trace(
                    go.Scatter(
                        x=X_VALS,
                        y=y_vals,
                        mode="lines",
                        name=grp_label,
                        line=dict(color=COLOURS[grp_key], width=2.5, dash=dash),
                        visible=visible,
                        legendgroup=grp_key,
                        showlegend=show_legend,
                    ),
                    row=1, col=col_num,
                )

    total_traces = sum(traces_per_mod)
    buttons = []
    trace_offset = 0

    for i, key in enumerate(mod_keys):
        cfg = MODERATOR_CONFIGS[key]
        n = traces_per_mod[i]
        visibility = [False] * total_traces
        for j in range(n):
            visibility[trace_offset + j] = True

        buttons.append(dict(
            label=cfg["label"],
            method="update",
            args=[
                {"visible": visibility},
                {"legend.title.text": cfg["label"]},
            ],
        ))
        trace_offset += n

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
            title_text=MODERATOR_CONFIGS[mod_keys[0]]["label"],
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
            tickvals=X_TICK_VALS,
            ticktext=X_TICK_TEXT,
            showgrid=True,
            gridcolor="#EEEEEE",
            row=1, col=col,
        )
        fig.update_yaxes(
            title_text="Predicted happiness" if col == 1 else "",
            range=[1, 7],
            tickvals=[1, 2, 3, 4, 5, 6, 7],
            showgrid=True,
            gridcolor="#EEEEEE",
            row=1, col=col,
        )

    return fig

import pandas as pd
import numpy as np


def load_panels():
    """
    Load and clean both panel datasets.
    Returns df1 (2010-2014), df2 (2015-2019), and df_combined.
    Age restricted to 10-15. Derived variables added here.
    """
    df1 = pd.read_csv("utils/panel_2010_2014.csv")
    df2 = pd.read_csv("utils/panel_2015_2019.csv")

    df1 = df1[df1["age"].between(10, 15)].copy()
    df2 = df2[df2["age"].between(10, 15)].copy()

    df1["panel"] = "2010–2014"
    df2["panel"] = "2015–2019"

    df_combined = pd.concat([df1, df2], ignore_index=True)

    return df1, df2, df_combined


def means_by_age(df, outcome):
    """Return mean of outcome by age."""
    return df.groupby("age")[outcome].mean().round(4)


# ---------------------------------------------------------------------------
# Moderator data for the toggle chart.
# Predicted happiness = intercept + b_x*x + b_mod*mod_val + b_int*x*mod_val
# Coefficients from Appendix 2, Panel 1 and Panel 2 columns.
# mod_val is the observed mean within each group, computed from the data.
# ---------------------------------------------------------------------------

X_VALS = list(range(0, 5))   # 0,1,2,3,4 — the five ordinal SM hour categories


def _predicted(coefs, x, mod_val):
    """Predicted happiness at a given x and moderator value."""
    return np.clip(
        coefs["intercept"]
        + coefs["b_x"]   * x
        + coefs["b_mod"] * mod_val
        + coefs["b_int"] * x * mod_val,
        1, 7
    )


def _group_mean(df, col, lo, hi):
    """Observed mean of col for rows where col is in [lo, hi)."""
    sub = df[(df[col] >= lo) & (df[col] < hi)][col].dropna()
    return sub.mean()


def build_moderator_data(df_combined):
    """
    Build predicted happiness lines for each moderator using appendix
    interaction coefficients and observed within-group means as mod_val.

    Returns a dict keyed by moderator name. Each value is:
        {
            label:  str,
            groups: [ {name, colour, p1: [y0..y4], p2: [y0..y4]}, ... ]
        }
    """
    mods = {}

    # ------------------------------------------------------------------
    # 1. Sex (binary: 0=Male, 1=Female)
    # Appendix coefficients:
    #   P1: intercept=6.002, b_x=-0.124, b_mod=0.050, b_int=-0.095
    #   P2: intercept=5.895, b_x=-0.171, b_mod=0.235, b_int=-0.121
    # ------------------------------------------------------------------
    sex_coefs = {
        "p1": {"intercept": 6.002, "b_x": -0.124, "b_mod": 0.050, "b_int": -0.095},
        "p2": {"intercept": 5.895, "b_x": -0.171, "b_mod": 0.235, "b_int": -0.121},
    }
    mods["sex"] = {
        "label": "Sex",
        "groups": [
            {
                "name": "Male",
                "colour": "#E8714C",
                "p1": [round(_predicted(sex_coefs["p1"], x, 0), 3) for x in X_VALS],
                "p2": [round(_predicted(sex_coefs["p2"], x, 0), 3) for x in X_VALS],
            },
            {
                "name": "Female",
                "colour": "#4C9BE8",
                "p1": [round(_predicted(sex_coefs["p1"], x, 1), 3) for x in X_VALS],
                "p2": [round(_predicted(sex_coefs["p2"], x, 1), 3) for x in X_VALS],
            },
        ],
    }

    # ------------------------------------------------------------------
    # 2. Self-esteem index (levels 2, 3, 4 — level 1 has only 4 obs)
    # mod_val = observed mean within each integer band (±0.5)
    # Appendix coefficients:
    #   P1: intercept=2.615, b_x=-0.308, b_mod=1.026, b_int=0.089
    #   P2: intercept=2.645, b_x=-0.578, b_mod=1.021, b_int=0.157
    # ------------------------------------------------------------------
    se_coefs = {
        "p1": {"intercept": 2.615, "b_x": -0.308, "b_mod": 1.026, "b_int": 0.089},
        "p2": {"intercept": 2.645, "b_x": -0.578, "b_mod": 1.021, "b_int": 0.157},
    }
    se_colours = ["#E8714C", "#E8B44C", "#4CAF50", "#4C9BE8"]
    se_labels  = ["Least positive", "Less positive", "More positive", "Most positive"]
    se_groups  = []
    for lvl, colour, lbl in zip([1, 2, 3, 4], se_colours, se_labels):
        mv = _group_mean(df_combined, "selfesteem_index", lvl - 0.5, lvl + 0.5)
        se_groups.append({
            "name": lbl,
            "colour": colour,
            "p1": [round(_predicted(se_coefs["p1"], x, mv), 3) for x in X_VALS],
            "p2": [round(_predicted(se_coefs["p2"], x, mv), 3) for x in X_VALS],
        })
    mods["selfesteem"] = {"label": "Self-esteem", "groups": se_groups}

    # ------------------------------------------------------------------
    # 3. SDQ — clinical bands, mod_val = observed mean within each band
    # Appendix coefficients:
    #   P1: intercept=6.705, b_x=-0.006, b_mod=-0.072, b_int=-0.010
    #   P2: intercept=6.974, b_x=-0.119, b_mod=-0.098, b_int=0.000
    # ------------------------------------------------------------------
    sdq_coefs = {
        "p1": {"intercept": 6.705, "b_x": -0.006, "b_mod": -0.072, "b_int": -0.010},
        "p2": {"intercept": 6.974, "b_x": -0.119, "b_mod": -0.098, "b_int":  0.000},
    }
    sdq_bands = [
        ("Normal (0–15)",     -1,  15, "#4C9BE8"),
        ("Borderline (16–19)", 15, 19, "#E8B44C"),
        ("Abnormal (20–40)",   19, 40, "#E8714C"),
    ]
    sdq_groups = []
    for name, lo, hi, colour in sdq_bands:
        mv = _group_mean(df_combined, "sdq_total", lo, hi + 1)
        sdq_groups.append({
            "name": name,
            "colour": colour,
            "p1": [round(_predicted(sdq_coefs["p1"], x, mv), 3) for x in X_VALS],
            "p2": [round(_predicted(sdq_coefs["p2"], x, mv), 3) for x in X_VALS],
        })
    mods["sdq"] = {"label": "SDQ", "groups": sdq_groups}

    # ------------------------------------------------------------------
    # 4. Physical health (discrete levels 1–5, mod_val = exact integer)
    # Appendix coefficients:
    #   P1: intercept=5.046, b_x=-0.403, b_mod=0.239, b_int=0.077
    #   P2: intercept=4.772, b_x=-0.550, b_mod=0.301, b_int=0.097
    # ------------------------------------------------------------------
    health_coefs = {
        "p1": {"intercept": 5.046, "b_x": -0.403, "b_mod": 0.239, "b_int": 0.077},
        "p2": {"intercept": 4.772, "b_x": -0.550, "b_mod": 0.301, "b_int": 0.097},
    }
    health_items = [
        (1, "Poor (1)",       "#E8714C"),
        (2, "Fair (2)",       "#E8B44C"),
        (3, "Good (3)",       "#4CAF50"),
        (4, "Very good (4)",  "#4C9BE8"),
        (5, "Excellent (5)",  "#7B4CE8"),
    ]
    health_groups = []
    for lvl, name, colour in health_items:
        health_groups.append({
            "name": name,
            "colour": colour,
            "p1": [round(_predicted(health_coefs["p1"], x, lvl), 3) for x in X_VALS],
            "p2": [round(_predicted(health_coefs["p2"], x, lvl), 3) for x in X_VALS],
        })
    mods["health"] = {"label": "Physical health", "groups": health_groups}

    # ------------------------------------------------------------------
    # 5. Parental relationship index (levels 1–4, mod_val = observed mean)
    # Appendix coefficients:
    #   P1: intercept=5.659, b_x=-0.209, b_mod=0.127, b_int=0.011
    #   P2: intercept=5.811, b_x=-0.390, b_mod=0.054, b_int=0.062
    # ------------------------------------------------------------------
    par_coefs = {
        "p1": {"intercept": 5.659, "b_x": -0.209, "b_mod": 0.127, "b_int": 0.011},
        "p2": {"intercept": 5.811, "b_x": -0.390, "b_mod": 0.054, "b_int": 0.062},
    }
    idx_colours = ["#E8714C", "#E8B44C", "#4CAF50", "#4C9BE8"]
    idx_labels  = ["Least positive", "Less positive", "More positive", "Most positive"]
    par_groups  = []
    for lvl, colour, lbl in zip([1, 2, 3, 4], idx_colours, idx_labels):
        mv = _group_mean(df_combined, "parent_index", lvl - 0.5, lvl + 0.5)
        par_groups.append({
            "name": lbl,
            "colour": colour,
            "p1": [round(_predicted(par_coefs["p1"], x, mv), 3) for x in X_VALS],
            "p2": [round(_predicted(par_coefs["p2"], x, mv), 3) for x in X_VALS],
        })
    mods["parent"] = {"label": "Parental relationship", "groups": par_groups}

    # ------------------------------------------------------------------
    # 6. Sibling relationship index (levels 1–4, mod_val = observed mean)
    # Appendix coefficients:
    #   P1: intercept=5.212, b_x=-0.236, b_mod=0.260, b_int=0.013
    #   P2: intercept=3.693, b_x=0.471,  b_mod=0.700, b_int=-0.191
    # ------------------------------------------------------------------
    sib_coefs = {
        "p1": {"intercept": 5.212, "b_x": -0.236, "b_mod": 0.260, "b_int":  0.013},
        "p2": {"intercept": 3.693, "b_x":  0.471, "b_mod": 0.700, "b_int": -0.191},
    }
    sib_groups = []
    for lvl, colour, lbl in zip([1, 2, 3, 4], idx_colours, idx_labels):
        mv = _group_mean(df_combined, "sib_index", lvl - 0.5, lvl + 0.5)
        sib_groups.append({
            "name": lbl,
            "colour": colour,
            "p1": [round(_predicted(sib_coefs["p1"], x, mv), 3) for x in X_VALS],
            "p2": [round(_predicted(sib_coefs["p2"], x, mv), 3) for x in X_VALS],
        })
    mods["siblings"] = {"label": "Sibling relationship", "groups": sib_groups}

    # ------------------------------------------------------------------
    # 7. Leisure activity index (6 bands matching original survey labels)
    # Each individual leisure item scored 0-5; index is mean across items.
    # mod_val = observed mean within each band.
    # Appendix coefficients:
    #   P1: intercept=5.692, b_x=-0.057, b_mod=0.169, b_int=-0.043
    #   P2: intercept=5.846, b_x=-0.387, b_mod=0.124, b_int=0.095
    # ------------------------------------------------------------------
    leisure_coefs = {
        "p1": {"intercept": 5.692, "b_x": -0.057, "b_mod": 0.169, "b_int": -0.043},
        "p2": {"intercept": 5.846, "b_x": -0.387, "b_mod": 0.124, "b_int":  0.095},
    }
    leisure_bands = [
        (0,   0.5,  "Never/almost never",      "#E8714C"),
        (0.5, 1.5,  "Once a year or less",      "#E8B44C"),
        (1.5, 2.5,  "Several times per year",   "#4CAF50"),
        (2.5, 3.5,  "At least once per month",  "#4C9BE8"),
        (3.5, 4.5,  "At least once per week",   "#7B4CE8"),
        (4.5, 5.1,  "Most days",                "#333333"),
    ]
    leisure_groups = []
    for lo, hi, name, colour in leisure_bands:
        mv = _group_mean(df_combined, "leisure_index", lo, hi)
        leisure_groups.append({
            "name":   name,
            "colour": colour,
            "p1": [round(_predicted(leisure_coefs["p1"], x, mv), 3) for x in X_VALS],
            "p2": [round(_predicted(leisure_coefs["p2"], x, mv), 3) for x in X_VALS],
        })
    mods["leisure"] = {"label": "Leisure activity", "groups": leisure_groups}

    # ------------------------------------------------------------------
    # 8. Bullying involvement (binary: 0=Not involved, 1=Involved)
    # mod_val = 0 or 1 exactly (binary variable)
    # Appendix coefficients:
    #   P1: intercept=6.216, b_x=-0.189, b_mod=-0.864, b_int=-0.128
    #   P2: intercept=6.220, b_x=-0.197, b_mod=-1.637, b_int=0.161
    # ------------------------------------------------------------------
    bully_coefs = {
        "p1": {"intercept": 6.216, "b_x": -0.189, "b_mod": -0.864, "b_int": -0.128},
        "p2": {"intercept": 6.220, "b_x": -0.197, "b_mod": -1.637, "b_int":  0.161},
    }
    mods["bullying"] = {
        "label": "Bullying involvement",
        "groups": [
            {
                "name": "Not involved",
                "colour": "#4C9BE8",
                "p1": [round(_predicted(bully_coefs["p1"], x, 0), 3) for x in X_VALS],
                "p2": [round(_predicted(bully_coefs["p2"], x, 0), 3) for x in X_VALS],
            },
            {
                "name": "Involved in bullying",
                "colour": "#E8714C",
                "p1": [round(_predicted(bully_coefs["p1"], x, 1), 3) for x in X_VALS],
                "p2": [round(_predicted(bully_coefs["p2"], x, 1), 3) for x in X_VALS],
            },
        ],
    }

    return mods

import pandas as pd
import numpy as np


def load_panels():
    """
    Load and clean both panel datasets.
    Returns df1 (2010-2014), df2 (2015-2019), and df_combined.
    Age is restricted to 10-15 throughout.
    """
    df1 = pd.read_csv("utils/panel_2010_2014.csv")
    df2 = pd.read_csv("utils/panel_2015_2019.csv")

    # Restrict to 10-15 (5 age-16 observations in panel 2 are dropped)
    df1 = df1[df1["age"].between(10, 15)].copy()
    df2 = df2[df2["age"].between(10, 15)].copy()

    df1["panel"] = "2010–2014"
    df2["panel"] = "2015–2019"

    df_combined = pd.concat([df1, df2], ignore_index=True)

    return df1, df2, df_combined


def means_by_age(df, outcome):
    """Return mean of outcome by age for a given dataframe."""
    return df.groupby("age")[outcome].mean().round(4)


def moderator_groups(df_combined):
    """
    For each continuous moderator, compute +/-1 SD split groups.
    Returns a dict of {moderator_key: {label, low_label, high_label,
    low_series, high_series}} where series are mean happiness by age.
    Sex is handled as a binary split.
    """
    moderators = {}

    continuous = {
        "selfesteem_index": ("Self-esteem", "Lower self-esteem (−1 SD)", "Higher self-esteem (+1 SD)"),
        "sdq_total": ("Mental health difficulties", "Fewer difficulties (−1 SD)", "More difficulties (+1 SD)"),
        "parent_index": ("Parental support", "Lower parental support (−1 SD)", "Higher parental support (+1 SD)"),
        "health": ("Physical health", "Poorer health (−1 SD)", "Better health (+1 SD)"),
    }

    ages = list(range(10, 16))

    for col, (label, low_label, high_label) in continuous.items():
        m = df_combined[col].mean()
        s = df_combined[col].std()
        low = df_combined[df_combined[col] <= m - s]
        high = df_combined[df_combined[col] >= m + s]
        moderators[col] = {
            "label": label,
            "low_label": low_label,
            "high_label": high_label,
            "low": low.groupby("age")["happiness_index"].mean().reindex(ages).round(3),
            "high": high.groupby("age")["happiness_index"].mean().reindex(ages).round(3),
        }

    # Sex: binary
    boys = df_combined[df_combined["sex"] == 0]
    girls = df_combined[df_combined["sex"] == 1]
    moderators["sex"] = {
        "label": "Sex",
        "low_label": "Boys",
        "high_label": "Girls",
        "low": boys.groupby("age")["happiness_index"].mean().reindex(ages).round(3),
        "high": girls.groupby("age")["happiness_index"].mean().reindex(ages).round(3),
    }

    return moderators

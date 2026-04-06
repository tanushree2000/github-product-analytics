import pandas as pd


def generate_insights(df: pd.DataFrame) -> list[str]:
    insights: list[str] = []

    if df.empty:
        return ["No repository data available to analyze."]

    working_df = df.copy()
    working_df["adoption_ratio"] = working_df["forks"] / working_df["stars"].replace(0, pd.NA)
    working_df["issue_intensity"] = working_df["open_issues"] / working_df["stars"].replace(0, pd.NA)

    ranked_by_stars = working_df.sort_values("stars", ascending=False).reset_index(drop=True)
    top_repo = ranked_by_stars.iloc[0]

    if len(ranked_by_stars) > 1 and ranked_by_stars.iloc[1]["stars"] > 0:
        second_repo = ranked_by_stars.iloc[1]
        star_multiple = top_repo["stars"] / second_repo["stars"]
        insights.append(
            f"{top_repo['name']} leads on popularity with {star_multiple:.1f}x the stars of "
            f"{second_repo['name']}, indicating a materially larger top-of-funnel developer reach."
        )
    else:
        insights.append(
            f"{top_repo['name']} leads on popularity based on total stars."
        )

    best_adoption = working_df.sort_values("adoption_ratio", ascending=False).iloc[0]
    insights.append(
        f"{best_adoption['name']} has the strongest forks-to-stars ratio "
        f"({best_adoption['adoption_ratio']:.2f}), suggesting a higher share of interested users "
        f"move from awareness to active usage or contribution."
    )

    highest_issue_load = working_df.sort_values("issue_intensity", ascending=False).iloc[0]
    insights.append(
        f"{highest_issue_load['name']} has the highest issue intensity "
        f"({highest_issue_load['issue_intensity']:.3f} issues per star), which can indicate either "
        f"heavier active development or greater maintenance burden relative to community size."
    )

    lowest_issue_load = working_df.sort_values("issue_intensity", ascending=True).iloc[0]
    insights.append(
        f"{lowest_issue_load['name']} shows the lowest issue intensity, which may reflect a more stable "
        f"maintenance profile or lower support complexity relative to its scale."
    )

    return insights
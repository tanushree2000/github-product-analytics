def generate_insights(df):
    insights = []

    # Popularity comparison
    top = df.sort_values(by="stars", ascending=False)
    if len(top) > 1:
        gap = top.iloc[0]["stars"] / top.iloc[1]["stars"]
        insights.append(
            f"{top.iloc[0]['name']} leads in popularity with {gap:.1f}x more stars than the next competitor."
        )

    # Adoption efficiency
    df["adoption_ratio"] = df["forks"] / df["stars"]
    best_adoption = df.sort_values(by="adoption_ratio", ascending=False).iloc[0]
    insights.append(
        f"{best_adoption['name']} shows highest adoption efficiency (forks-to-stars ratio)."
    )

    # Development load
    high_issue = df.sort_values(by="open_issues", ascending=False).iloc[0]
    insights.append(
        f"{high_issue['name']} has the highest issue load, indicating active development but potential maintenance complexity."
    )

    return insights
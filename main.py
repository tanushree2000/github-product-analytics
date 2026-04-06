import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_fetcher import fetch_repo_data
from insight_engine import generate_insights


DEFAULT_REPOS = [
    "pytorch/pytorch",
    "tensorflow/tensorflow",
    "scikit-learn/scikit-learn",
]


def parse_repos() -> list[str]:
    repos = sys.argv[1:]
    return repos if repos else DEFAULT_REPOS


def build_dataframe(repos: list[str]) -> pd.DataFrame:
    repo_list: list[dict] = []

    for repo in repos:
        repo_data = fetch_repo_data(repo)
        if repo_data is not None:
            repo_list.append(repo_data)

    return pd.DataFrame(repo_list)


def print_summary(df: pd.DataFrame) -> None:
    if df.empty:
        print("\nNo valid repository data fetched.")
        return

    display_df = df.copy()
    display_df["adoption_ratio"] = display_df["forks"] / display_df["stars"].replace(0, pd.NA)
    print("\nRepository Comparison:")
    print(display_df.to_string(index=False))


def plot_normalized_metrics(df: pd.DataFrame, output_file: str = "output.png") -> None:
    if df.empty:
        print("[WARN] Skipping visualization because the dataframe is empty.")
        return

    plot_df = df.copy()
    metrics = ["stars", "forks", "open_issues"]

    normalized_df = plot_df.copy()
    for col in metrics:
        max_value = normalized_df[col].max()
        normalized_df[col] = normalized_df[col] / max_value if max_value else 0

    repos = normalized_df["name"]
    x = np.arange(len(repos))
    width = 0.24

    fig, ax = plt.subplots(figsize=(11, 6.5))

    colors = {
        "stars": "#4C78A8",
        "forks": "#F58518",
        "open_issues": "#54A24B",
    }

    ax.bar(x - width, normalized_df["stars"], width, label="Popularity (Stars)", color=colors["stars"])
    ax.bar(x, normalized_df["forks"], width, label="Adoption (Forks)", color=colors["forks"])
    ax.bar(
        x + width,
        normalized_df["open_issues"],
        width,
        label="Activity (Open Issues)",
        color=colors["open_issues"],
    )

    fig.suptitle(
        "Relative Comparison of Repository Performance Across Key Metrics",
        fontsize=15,
        fontweight="bold",
        y=0.97,
    )
    ax.set_title(
        "Metrics are normalized to a 0–1 scale so lower-magnitude signals remain visible",
        fontsize=10,
        color="#6B7280",
        pad=14,
    )

    ax.set_xlabel("Repository")
    ax.set_ylabel("Normalized Value (0–1)")
    ax.set_xticks(x)
    ax.set_xticklabels(repos)

    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.show()

    print(f"\nSaved chart to: {Path(output_file).resolve()}")


def main() -> None:
    repos = parse_repos()
    df = build_dataframe(repos)

    if df.empty:
        print("\nNo valid repositories were fetched. Exiting.")
        return

    print_summary(df)

    print("\nInsights:")
    for insight in generate_insights(df):
        print(f"- {insight}")

    plot_normalized_metrics(df)


if __name__ == "__main__":
    main()
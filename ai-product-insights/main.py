import pandas as pd
from data_fetcher import fetch_repo_data
from insight_engine import generate_insights
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# =========================
# STEP 1: FETCH DATA
# =========================

repos = [
    "pytorch/pytorch",
    "tensorflow/tensorflow",
    "scikit-learn/scikit-learn"
]

repo_list = []

for repo in repos:
    repo_list.append(fetch_repo_data(repo))

# =========================
# STEP 2: CREATE DATAFRAME
# =========================

df = pd.DataFrame(repo_list)

print("\nRepository Comparison:")
print(df.to_string(index=False))

# =========================
# STEP 3: INSIGHTS
# =========================

print("\nInsights:")
insights = generate_insights(df)

for insight in insights:
    print(f"- {insight}")

# =========================
# STEP 4: VISUALIZATION (FIXED VERSION)
# =========================

repos = df["name"]
stars = df["stars"]
forks = df["forks"]
issues = df["open_issues"]

x = np.arange(len(repos))
width = 0.25

# Figure
plt.figure(figsize=(10, 6))

# Colors
colors = {
    "stars": "#4C78A8",
    "forks": "#F58518",
    "issues": "#54A24B"
}

# Bars
bars1 = plt.bar(x - width, stars, width, label="Stars", color=colors["stars"])
bars2 = plt.bar(x, forks, width, label="Forks", color=colors["forks"])
bars3 = plt.bar(x + width, issues, width, label="Open Issues", color=colors["issues"])

# =========================
# TITLE FIX (NO OVERLAP)
# =========================

plt.suptitle(
    "Repository Comparison Across Popularity, Usage, and Activity",
    fontsize=14,
    weight='bold',
    y=0.98
)

plt.title(
    "GitHub metrics for leading ML repositories",
    fontsize=10,
    color="#6B7280",
    pad=20
)

# =========================
# AXIS
# =========================

plt.xlabel("Repository")
plt.ylabel("Count")
plt.xticks(x, repos)

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Grid
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Legend
plt.legend(frameon=False)

# Value labels
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{int(height):,}",
            ha='center',
            va='bottom',
            fontsize=8
        )

add_labels(bars1)
add_labels(bars2)
add_labels(bars3)

# Clean look
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Layout fix (IMPORTANT)
plt.tight_layout(rect=[0, 0, 1, 0.90])

plt.show()
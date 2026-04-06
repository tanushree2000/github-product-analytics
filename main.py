import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from data_fetcher import fetch_repo_data
from insight_engine import generate_insights

# =========================
# INPUT (DYNAMIC)
# =========================

repos = sys.argv[1:]

if not repos:
    print("Usage: python main.py owner/repo owner/repo")
    sys.exit()

# =========================
# FETCH DATA
# =========================

repo_list = []

for repo in repos:
    data = fetch_repo_data(repo)
    if data:
        repo_list.append(data)

df = pd.DataFrame(repo_list)

# =========================
# INSIGHTS
# =========================

print("\nInsights:")
for insight in generate_insights(df):
    print(f"- {insight}")

# =========================
# NORMALIZATION (FIX SCALE ISSUE)
# =========================

df_norm = df.copy()
for col in ["stars", "forks", "open_issues"]:
    df_norm[col] = df[col] / df[col].max()

# =========================
# VISUALIZATION
# =========================

repos = df["name"]
x = np.arange(len(repos))
width = 0.25

plt.figure(figsize=(10, 6))

colors = {
    "stars": "#4C78A8",
    "forks": "#F58518",
    "issues": "#54A24B"
}

bars1 = plt.bar(x - width, df_norm["stars"], width, label="Popularity (Stars)", color=colors["stars"])
bars2 = plt.bar(x, df_norm["forks"], width, label="Adoption (Forks)", color=colors["forks"])
bars3 = plt.bar(x + width, df_norm["open_issues"], width, label="Activity (Issues)", color=colors["issues"])

# Titles
plt.suptitle(
    "Relative Comparison of ML Repositories Across Key Metrics",
    fontsize=14,
    weight='bold',
    y=0.98
)

plt.title(
    "Values normalized (0–1) to enable fair comparison across different scales",
    fontsize=10,
    color="#6B7280",
    pad=15
)

# Axis
plt.xticks(x, repos)
plt.ylabel("Relative Scale (0–1)")

# Grid
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Legend
plt.legend(frameon=False)

# Clean look
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.92])

plt.show()
import requests
import os


def fetch_repo_data(repo_name: str, timeout: int = 10) -> dict | None:
    url = f"https://api.github.com/repos/{repo_name}"

    # =========================
    # ADD GITHUB TOKEN SUPPORT
    # =========================
    headers = {}
    token = os.environ.get("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        # =========================
        # ERROR HANDLING
        # =========================

        if response.status_code == 404:
            print(f"[WARN] Repository not found: {repo_name}")
            return None

        if response.status_code == 403:
            print(
                f"[WARN] Rate limit or access issue for {repo_name}. "
                f"Consider setting GITHUB_TOKEN environment variable."
            )
            return None

        if response.status_code != 200:
            print(f"[WARN] Failed to fetch {repo_name}. Status code: {response.status_code}")
            return None

        data = response.json()

        # =========================
        # CLEAN DATA RETURN
        # =========================

        return {
            "full_name": repo_name,
            "name": data.get("name", repo_name.split("/")[-1]),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0),
        }

    # =========================
    # EXCEPTION HANDLING
    # =========================

    except requests.exceptions.Timeout:
        print(f"[WARN] Request timed out for {repo_name}")
        return None

    except requests.exceptions.RequestException as exc:
        print(f"[WARN] Request failed for {repo_name}: {exc}")
        return None

    except ValueError as exc:
        print(f"[WARN] Invalid JSON received for {repo_name}: {exc}")
        return None
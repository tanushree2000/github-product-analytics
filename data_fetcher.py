import requests


def fetch_repo_data(repo_name: str, timeout: int = 10) -> dict | None:
    url = f"https://api.github.com/repos/{repo_name}"

    try:
        response = requests.get(url, timeout=timeout)

        if response.status_code == 404:
            print(f"[WARN] Repository not found: {repo_name}")
            return None

        if response.status_code == 403:
            print(
                f"[WARN] Access/rate limit issue for {repo_name}. "
                f"Status code: {response.status_code}"
            )
            return None

        if response.status_code != 200:
            print(f"[WARN] Failed to fetch {repo_name}. Status code: {response.status_code}")
            return None

        data = response.json()

        return {
            "full_name": repo_name,
            "name": data.get("name", repo_name.split("/")[-1]),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0),
        }

    except requests.exceptions.Timeout:
        print(f"[WARN] Request timed out for {repo_name}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"[WARN] Request failed for {repo_name}: {exc}")
        return None
    except ValueError as exc:
        print(f"[WARN] Invalid JSON received for {repo_name}: {exc}")
        return None
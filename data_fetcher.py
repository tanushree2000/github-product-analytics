import requests

def fetch_repo_data(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error fetching {repo_name}: {response.status_code}")
            return None

        data = response.json()

        return {
            "name": data.get("name"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0)
        }

    except Exception as e:
        print(f"Exception occurred for {repo_name}: {e}")
        return None
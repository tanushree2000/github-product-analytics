import requests

def fetch_repo_data(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(url)
    data = response.json()

    return {
        "name": data["name"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "watchers": data["watchers_count"],
        "open_issues": data["open_issues_count"]
    }
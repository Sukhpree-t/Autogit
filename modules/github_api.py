import requests

class GitHubAPI:

    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.base = "https://api.github.com"

    def create_repo(self, repo_name):

        url = f"{self.base}/user/repos"

        payload = {
            "name": repo_name,
            "private": False
        }

        r = requests.post(url, json=payload, auth=(self.username, self.token))

        if r.status_code == 201:
            return "Repository created successfully on GitHub"
        else:
            return f"GitHub error: {r.text}"

    def list_repos(self):

        url = f"{self.base}/user/repos"

        r = requests.get(url, auth=(self.username, self.token))

        if r.status_code == 200:

            repos = []

            for repo in r.json():
                repos.append(repo["name"])

            return repos

        return ["Error fetching repositories"]

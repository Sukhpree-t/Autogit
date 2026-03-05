from git import Repo
import os
import requests

class RepoManager:

    def get_repos(self, username, token=None):
        if token:
            url = "https://api.github.com/user/repos"
            headers = {"Authorization": f"token {token}"}
            response = requests.get(url, headers=headers)
        else:
            url = f"https://api.github.com/users/{username}/repos"
            response = requests.get(url)
        
        if response.status_code == 200:
            repos = response.json()
            return [repo["name"] for repo in repos]
        return []

    def init_repo(self, path, username, repo, token=None):
        # Use token for HTTPS if provided, otherwise default to SSH
        if token:
            url = f"https://{token}@github.com/{username}/{repo}.git"
        else:
            url = f"git@github.com:{username}/{repo}.git"

        if not os.path.exists(path):
            os.makedirs(path)

        # Initialize or open existing repo
        if not os.path.exists(os.path.join(path,'.git')):
            repo_obj=Repo.init(path)
            # Modern GitHub default is 'main'
            try:
                repo_obj.git.branch("-M", "main")
            except:
                pass
        else:
            repo_obj = Repo(path)

        # Ensure 'origin' remote is correct
        if 'origin' in [r.name for r in repo_obj.remotes]:
            repo_obj.remotes.origin.set_url(url)
        else:
            repo_obj.create_remote("origin", url)

        # Initial commit and Force Push to establish the link
        try:
            repo_obj.git.add("--all")
            if repo_obj.is_dirty(untracked_files=True) or len(repo_obj.untracked_files) > 0:
                repo_obj.index.commit("Initial commit via AutoGit")
            
            branch_name = repo_obj.active_branch.name
            repo_obj.git.push("-u", "origin", branch_name, "--force")
            return f"Repo initialized and Force Pushed to '{branch_name}'"
        except Exception as e:
            return f"Init failed during push: {str(e)}"

    def push(self,path):
        try:
            if not os.path.exists(os.path.join(path, '.git')):
                return "Error: Not a git repository. Click 'Init Repo' first."
            
            repo=Repo(path)
            
            if 'origin' not in [r.name for r in repo.remotes]:
                return "Error: Remote 'origin' not found. Click 'Init Repo'."

            repo.git.add("--all")

            if repo.is_dirty(untracked_files=True) or len(repo.untracked_files) > 0:
                try:
                    repo.index.commit("Auto commit")
                except Exception as e:
                    if "nothing to commit" in str(e).lower():
                        return "No changes to commit"
                    return f"Commit failed: {str(e)}"
                
                try:
                    # Automatically detect active branch
                    branch_name = repo.active_branch.name
                    
                    try:
                        # Try standard push first
                        repo.git.push('origin', branch_name, u=True)
                        return f"Push success ({branch_name})"
                    except Exception:
                        # Fallback: Force push to bypass merge conflicts
                        # This replaces remote history with local state
                        repo.git.push('origin', branch_name, "--force")
                        return f"Force Push success ({branch_name})"
                except Exception as e:
                    return f"Push failed: {str(e)}"

            return "No changes to commit"
        except Exception as e:
            return f"Error: {str(e)}"

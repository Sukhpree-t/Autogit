import tkinter as tk
from tkinter import filedialog, ttk
from modules.repo_manager import RepoManager
from modules.auto_commit import AutoCommit
from modules.settings_manager import load, save

class App:

    def __init__(self,root):
        self.root=root
        self.root.title("AutoGit SSH")

        self.repo_manager=RepoManager()
        self.auto=None

        self.settings=load()

        self.build()

    def build(self):

        tk.Label(text="GitHub Username").pack()
        self.username=tk.Entry(width=40)
        self.username.pack()
        self.username.insert(0,self.settings["username"])

        tk.Label(text="GitHub Token (optional, for private repos)").pack()
        self.token=tk.Entry(width=40, show="*")
        self.token.pack()
        self.token.insert(0,self.settings.get("token", ""))

        tk.Label(text="Repository Name").pack()
        repo_frame = tk.Frame(self.root)
        repo_frame.pack()
        self.repo = ttk.Combobox(repo_frame, width=37)
        self.repo.pack(side="left")
        self.repo.insert(0, self.settings["repo_name"])
        tk.Button(repo_frame, text="Fetch", command=self.fetch_repos).pack(side="left")

        tk.Label(text="Local Folder").pack()

        frame=tk.Frame()
        frame.pack()

        self.path=tk.Entry(frame,width=35)
        self.path.pack(side="left")
        self.path.insert(0,self.settings["repo_path"])

        tk.Button(frame,text="Browse",command=self.browse).pack(side="left")

        tk.Label(text="Commit Interval (minutes)").pack()
        self.interval=tk.Entry(width=10)
        self.interval.pack()
        self.interval.insert(0,self.settings["commit_interval"])

        btn=tk.Frame()
        btn.pack(pady=10)

        tk.Button(btn,text="Init Repo",command=self.init_repo).grid(row=0,column=0)
        tk.Button(btn,text="Push Now",command=self.push).grid(row=0,column=1)

        tk.Button(btn,text="Start Auto",command=self.start_auto).grid(row=1,column=0)
        tk.Button(btn,text="Stop Auto",command=self.stop_auto).grid(row=1,column=1)

        tk.Button(btn,text="Clear Logs",command=self.clear_logs).grid(row=2,column=0,columnspan=2,pady=5)

        self.log=tk.Text(height=12,width=80)
        self.log.pack()

    def log_msg(self,msg):
        self.log.insert(tk.END,msg+"\n")
        self.log.see(tk.END)

    def fetch_repos(self):
        username = self.username.get()
        token = self.token.get()
        if not username and not token:
            self.log_msg("Enter username or token first")
            return
        self.log_msg(f"Fetching repos...")
        try:
            repos = self.repo_manager.get_repos(username, token)
            if repos:
                self.repo['values'] = repos
                self.log_msg(f"Found {len(repos)} repositories")
            else:
                self.log_msg("No repositories found or error occurred")
        except Exception as e:
            self.log_msg(f"Error fetching repos: {str(e)}")

    def browse(self):
        folder=filedialog.askdirectory()
        if folder:
            self.path.delete(0,"end")
            self.path.insert(0,folder)

    def save_settings(self):
        data={
            "username":self.username.get(),
            "token":self.token.get(),
            "repo_name":self.repo.get(),
            "repo_path":self.path.get(),
            "commit_interval":self.interval.get()
        }
        save(data)

    def init_repo(self):
        self.save_settings()
        msg=self.repo_manager.init_repo(self.path.get(),self.username.get(),self.repo.get(),self.token.get())
        self.log_msg(msg)

    def push(self):
        msg=self.repo_manager.push(self.path.get())
        self.log_msg(msg)

    def start_auto(self):
        self.auto=AutoCommit(self.repo_manager,self.path.get(),int(self.interval.get()),self.log_msg)
        self.auto.start()
        self.log_msg("Auto commit started")

    def stop_auto(self):
        if self.auto:
            self.auto.stop()
            self.log_msg("Auto commit stopped")

    def clear_logs(self):
        self.log.delete("1.0", tk.END)

root=tk.Tk()
app=App(root)
root.mainloop()

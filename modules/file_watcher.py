from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):

    def __init__(self, repo_manager, path, logger):
        self.repo_manager=repo_manager
        self.path=path
        self.logger=logger

    def on_any_event(self,event):
        if not event.is_directory:
            msg=self.repo_manager.push(self.path)
            self.logger("File changed → "+msg)

class Watcher:

    def __init__(self, repo_manager, path, logger):
        self.repo_manager=repo_manager
        self.path=path
        self.logger=logger
        self.obs=Observer()

    def start(self):
        handler=Handler(self.repo_manager,self.path,self.logger)
        self.obs.schedule(handler,self.path,recursive=True)
        self.obs.start()

    def stop(self):
        self.obs.stop()
        self.obs.join()

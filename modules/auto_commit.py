import schedule, threading, time

class AutoCommit:

    def __init__(self, repo_manager, path, interval, logger):
        self.repo_manager=repo_manager
        self.path=path
        self.interval=interval
        self.logger=logger
        self.running=False

    def job(self):
        msg=self.repo_manager.push(self.path)
        self.logger(msg)

    def start(self):
        self.running=True
        schedule.every(self.interval).minutes.do(self.job)

        def loop():
            while self.running:
                schedule.run_pending()
                time.sleep(1)

        threading.Thread(target=loop,daemon=True).start()

    def stop(self):
        self.running=False

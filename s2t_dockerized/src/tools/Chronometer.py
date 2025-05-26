import time

class Chronometer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.perf_counter() - self.elapsed_time
            self.running = True

    def pause(self):
        if self.running:
            self.elapsed_time = time.perf_counter() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def get_time(self, decimals=2):
        if self.running:
            return round(time.perf_counter() - self.start_time, decimals)
        return round(self.elapsed_time, decimals)
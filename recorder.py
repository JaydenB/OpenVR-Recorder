import numpy


class Recorder(object):
    def __init__(self):
        self.live = False

        self.buffer = []

    def start_recording(self):
        if self.live:
            return
        self.live = True

    def stop_recording(self):
        if not self.live:
            return
        self.live = False

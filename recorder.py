import numpy
import sys


class Recorder(object):
    def __init__(self):
        self.buffer = []

    def end_recording(self, file_path, slate_data):

        slate = "%s.%s.tk%s" % (slate_data[0], slate_data[1], slate_data[2])
        print("File path: %s" % file_path)
        print(f"File Path: {file_path}")
        print("Slate: %s" % slate)
        print("Sample Count: %s, Length: %s seconds, Avg: %s per second" % (
            len(self.buffer),
            round(self.buffer[-1]["time"]-self.buffer[0]["time"], 2),
            len(self.buffer)/round(self.buffer[-1]["time"]-self.buffer[0]["time"], 2)
        ))
        print("Disk Size: %sMB" % round(sys.getsizeof(self.buffer)/1048576, 4))

        print("")

        for sample in self.buffer:
            print("%ssecs - %s" % (
                round(sample.get("time")-self.buffer[0].get("time"), 2),
                sample.get("tracker_1")))
        print("finished printing buffer data")

        self.buffer = []
        print("cleared buffer")

    def add_sample(self, sample):
        self.buffer.append(sample)

import triad_openvr
import time

from PyQt5 import QtCore


class ListenerWorker(QtCore.QObject):
    obtained_sample = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.interval = 1/250

        self.vr = None
        self.active = True

    def start(self):
        print("Starting Listener Thread")

        # self.vr = triad_openvr.triad_openvr()

        self.main_loop()
        self.finished.emit()

    def main_loop(self):
        i = 0
        while self.active:
            start_time = time.time()

            i += 1
            # self.obtained_sample.emit("%s %s" % (start_time, i))

            sleep_time = self.interval - (time.time() - start_time)
            if sleep_time > 0:
                # QtCore.QThread.msleep(int(sleep_time*1000))
                time.sleep(sleep_time)
        print(i)

    def close(self):
        # self.vr.close_triad()

        self.active = False
        print("Active CLOSED: %s" % self.active)


if __name__ == '__main__':
    # interval = 1/refresh_rate
    #
    # v = vr.triad_openvr()
    # v.print_discovered_objects()
    #
    # while True:
    #     start = time.time()
    #     text = ""
    #     for pose in v.devices[device_name].get_pose_euler():
    #         text += "%s.4f" % pose
    #         text += " "
    #     print("\r" + text, end="")
    #     sleep_time = interval-(time.time()-start)
    #     if sleep_time > 0:
    #         time.sleep(sleep_time)
    pass

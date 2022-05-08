import triad_openvr
import time

from PyQt5 import QtCore


class ListenerWorker(QtCore.QObject):
    obtained_sample = QtCore.pyqtSignal(dict)
    obtained_devices = QtCore.pyqtSignal(dict)
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.interval = 1/120

        self.vr = None
        self.active = False
        self.looping = True

    def start(self):
        print("Starting Listener Thread")

        # self.vr = triad_openvr.triad_openvr()

        self.main_loop()
        self.finished.emit()

    def main_loop(self):
        while self.looping:
            if self.active:
                start_time = time.time()

                poses = dict()
                for device in self.vr.devices.keys():
                    poses[device] = self.vr.devices[device].get_pose_euler()
                poses["time"] = time.time()
                self.obtained_sample.emit(poses)

                # SLEEP UNTIL NEXT UPDATE
                sleep_time = self.interval - (time.time() - start_time)
                if sleep_time > 0:
                    # QtCore.QThread.msleep(int(sleep_time*1000))
                    time.sleep(sleep_time)
            else:
                time.sleep(0.1)

    def start_active(self):
        self.vr = triad_openvr.triad_openvr()
        self.obtained_devices.emit(self.vr.devices)

        self.active = True

        print("Active STARTED: %s" % self.active)

    def close_active(self):
        self.active = False
        self.vr.close_triad()
        self.vr = None
        print("Active CLOSED: %s" % self.active)

    def kill(self):
        self.looping = False

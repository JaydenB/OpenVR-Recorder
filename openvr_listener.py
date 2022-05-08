import triad_openvr
import time
import numpy as np

from PyQt5 import QtCore


def matmult_b_to_local_a(a, b):
    bb = np.array([b[0], b[1], b[2], [0,0,0,1]])
    new = np.matmul(a, bb)
    local_b_list = new.tolist()
    return [local_b_list[0], local_b_list[1], local_b_list[2]]


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
        self.last_poses = None

        # self.root = np.array([
        #     [-0.5815409421920776, 0.8135089874267578, -0.0036786096170544624, -1.8250683546066284],
        #     [0.00013452331768348813, -0.004425797611474991, -0.9999902844429016, -0.6333032846450806],
        #     [-0.8135173320770264, -0.5815356373786926, 0.0024641845375299454, -1.8179576396942139],
        #     [0, 0, 0, 1]
        # ])
        # self.inv_root = np.linalg.inv(self.root)
        self.root = None
        self.inv_root = None

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

                    # Standard 3x4 Position Rotation Matrix
                    m = self.vr.devices[device].get_pose_matrix()

                    # transform to local around calibration point if it exists
                    local_m = m
                    if self.inv_root is not None:
                        local_m = matmult_b_to_local_a(self.inv_root, m)

                    poses[device] = {
                        "raw_matrix": [list(m[0]), list(m[1]), list(m[2])],
                        "matrix": local_m,
                        "position": [local_m[0][3], local_m[1][3], local_m[2][3]],
                        "euler": triad_openvr.convert_to_euler(local_m),
                        "quaternion": triad_openvr.convert_to_quaternion(local_m)
                    }
                poses["time"] = time.time()
                self.obtained_sample.emit(poses)
                self.last_poses = poses

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

        # Clear Calibration
        self.root = None
        self.inv_root = None

        self.active = True

        print("Active STARTED: %s" % self.active)

    def close_active(self):
        self.active = False
        self.vr.close_triad()
        self.vr = None

        # Clear Calibration
        self.root = None
        self.inv_root = None

        print("Active CLOSED: %s" % self.active)

    def kill(self):
        self.looping = False

    # -------------------------------------------------------------------------

    def capture_calibration(self):
        print("attempting calibration")
        if self.last_poses is None:
            print("Cannot Capture Calibration Point - no previous point exists.")
            return

        self.root = None
        self.inv_root = None

        # print("using previous pose: %s" % self.last_poses['tracker_1'])
        # print(self.last_poses['tracker_1']['raw_matrix'])
        temp_root = self.last_poses.get('tracker_1')['raw_matrix']
        self.root = np.array([temp_root[0], temp_root[1],
                              temp_root[2], [0, 0, 0, 1]])
        self.inv_root = np.linalg.inv(self.root)

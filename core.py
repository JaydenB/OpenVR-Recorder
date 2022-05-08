from PyQt5 import QtWidgets, QtGui, QtCore
import os

import ui.recorder_widget as rcw
import device
import settings
import recorder
import openvr_listener as vr
from datetime import datetime


class RecorderApplication(QtWidgets.QApplication):
    close_connection = QtCore.pyqtSignal()
    open_connection = QtCore.pyqtSignal()

    start_recording = QtCore.pyqtSignal()
    stop_recording = QtCore.pyqtSignal()
    capture_calibration = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QApplication.__init__(self, [])
        self.setApplicationName("OpenVR Recorder")
        self.setWindowIcon(QtGui.QIcon("./ui/icons/application.png"))

        self.settings = settings.Settings()

        self.ui_widget = rcw.RecorderWidget()
        self.ui_widget.show()

        self.connected = False
        self.recording = False

        # --------------------------------------------------------
        #   Threaded listening

        self.listener_thread = QtCore.QThread()
        self.listener_worker = vr.ListenerWorker()

        self.capture_calibration.connect(self.listener_worker.capture_calibration)
        self.open_connection.connect(self.listener_worker.start_active)
        self.close_connection.connect(self.listener_worker.close_active)
        self.listener_worker.moveToThread(self.listener_thread)

        self.listener_worker.finished.connect(self.listener_thread.quit)
        self.listener_worker.finished.connect(self.listener_worker.deleteLater)
        self.listener_thread.finished.connect(self.listener_thread.deleteLater)

        self.listener_thread.started.connect(self.listener_worker.start)
        self.listener_thread.finished.connect(self.listener_worker.kill)

        self.listener_worker.obtained_devices.connect(self.create_devices)
        self.listener_worker.obtained_sample.connect(self.obtained_sample)

        self.listener_thread.start()

        # --------------------------------------------------------

        self.recorder = recorder.Recorder()

        self._vr = None
        self._tracked_devices = []

        # Connect UI Signals
        self.ui_widget.pb_calibrate.clicked.connect(self.calibrate_volume)
        self.ui_widget.pb_record.clicked.connect(self.recording_toggle)
        self.ui_widget.pb_connection.clicked.connect(self.connection_toggle)

    # -----------------------------------------
    #   Calibration
    # -----------------------------------------

    def calibrate_volume(self):
        self.capture_calibration.emit()

    # -----------------------------------------
    #   Recording
    # -----------------------------------------

    def recording_toggle(self):
        if self.recording:
            self.recording_stop()
        else:
            if self.connected:
                self.recording_start()

    def recording_start(self):
        self.recording = True
        self.ui_widget.update_record_icon(self.recording)

        print("Starting Recording...")
        self.start_recording.emit()

    def recording_stop(self):
        print("Ending Recording!\n")
        self.recording = False
        self.ui_widget.update_record_icon(self.recording)

        slate_data = self.get_slate_data()
        file_path = self.create_filepath()

        # self.stop_recording.emit()
        self.recorder.end_recording(file_path, slate_data,
                                    self.listener_worker.root.tolist())

        self.ui_widget.sb_take.setValue(slate_data[2]+1)

    # -----------------------------------------
    #   OpenVR Connection
    # -----------------------------------------

    def connection_toggle(self):
        if self.connected:
            if self.recording:
                self.recording_stop()
            self.openvr_disconnect()
        else:
            self.openvr_connect()

    def openvr_connect(self):
        self.connected = True
        self.ui_widget.update_connected_icon(self.connected)

        # self.create_devices(self._vr.devices)
        self.open_connection.emit()

        print("OpenVR Connected!")

    def openvr_disconnect(self):
        self.connected = False
        self.ui_widget.update_connected_icon(self.connected)

        self.close_connection.emit()

        self.remove_devices()
        # self._vr = None
        print("OpenVR Disconnected!")

    # -----------------------------------------
    #   UI Connections
    # -----------------------------------------

    def create_filepath(self):
        # date = datetime.now().date()
        # return f"{self.ui_widget.file_browser.le_filepath.text()}/" \
        #        f"{date.year}_{date.month}_{date.day}"
        return self.ui_widget.file_browser.le_filepath.text()

    def get_takes(self):
        # @TODO: Get all recorded takes at current filepath in slate/setup/take order
        return []

    def update_takes(self):
        # @TODO: Run check on self.get_takes() return and increment take if already exists
        return None

    # -----------------------------------------------------------

    def create_devices(self, devices):
        print("Devices: %s" % list(devices.keys()))
        for d in devices.keys():
            print("Creating new Device for '%s'" % d)
            new_device = device.TrackedDevice(self, d)
            self._tracked_devices.append(new_device)

    def remove_devices(self):
        self.ui_widget.clear_devices()
        self._tracked_devices = []

    def obtained_sample(self, sample):
        # print("Sample: %s" % sample)
        recorded_sample = dict()
        recorded_sample["time"] = sample.get("time", 0.0)
        for sample_device in sample.keys():
            for d in self._tracked_devices:
                if d.name == sample_device:
                    pose = sample.get(sample_device).get('euler')
                    d.update_pose(pose)
                    if self.recording:
                        recorded_sample[d.name] = sample.get(sample_device)
        if self.recording:
            self.recorder.add_sample(recorded_sample)

    def get_slate_data(self):
        return [self.ui_widget.le_slate.text(),
                self.ui_widget.le_setup.text(),
                self.ui_widget.sb_take.value()]


if __name__ == "__main__":
    app = RecorderApplication()
    app.exec_()

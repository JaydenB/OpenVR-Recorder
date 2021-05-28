from PyQt5 import QtWidgets, QtGui
import triad_openvr
import os

import ui.recorder_widget as rcw
import device
import settings
import recorder


class RecorderApplication(QtWidgets.QApplication):
    def __init__(self):
        QtWidgets.QApplication.__init__(self, [])
        self.setApplicationName("OpenVR Recorder")
        self.setWindowIcon(QtGui.QIcon("./ui/icons/application.png"))

        self.settings = settings.Settings()

        self.ui_widget = rcw.RecorderWidget()
        self.ui_widget.show()

        self.connected = False
        self.recording = False

        self.recorder = recorder.Recorder()

        self._vr = None
        self._tracked_devices = []

        # Connect UI Signals
        self.ui_widget.pb_record.clicked.connect(self.recording_toggle)
        self.ui_widget.pb_connection.clicked.connect(self.connection_toggle)

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
        # if self._vr is None:
        #     # @TODO: Not connected properly
        #     return
        self.recording = True
        self.ui_widget.update_record_icon(self.recording)

        print("Starting Recording...")
        self.recorder.start_recording()

    def recording_stop(self):
        self.recording = False
        self.ui_widget.update_record_icon(self.recording)

        print("Ending Recording!")
        self.recorder.stop_recording()

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

        # self._vr = triad_openvr.triad_openvr()
        # self.create_devices(self._vr.devices)

        print("OpenVR Connected!")

    def openvr_disconnect(self):
        self.connected = False
        self.ui_widget.update_connected_icon(self.connected)

        self.remove_devices()
        self._vr = None
        print("OpenVR Disconnected!")

    # -----------------------------------------
    #   UI Connections
    # -----------------------------------------

    def create_filepath(self):
        return os.path.join(*[
            self.ui_widget.file_browser.le_filepath.text,
            self.ui_widget.le_slate.text,
            self.ui_widget.le_setup.text,
            str(self.ui_widget.sb_take.value)])

    def get_takes(self):
        # @TODO: Get all recorded takes at current filepath in slate/setup/take order
        return []

    def update_takes(self):
        # @TODO: Run check on self.get_takes() return and increment take if already exists
        return None

    # -----------------------------------------------------------

    def create_devices(self, devices):
        if self._vr is not None:
            self._vr.print_discovered_objects()
            print(devices)
            for d in devices.keys():
                new_device = device.TrackedDevice(self, d)
                self._tracked_devices.append(new_device)

    def remove_devices(self):
        self.ui_widget.clear_devices()
        self._tracked_devices = []


# 250 Hz refresh rate of data
refresh_rate = 250
device_name = "tracker_1"


if __name__ == "__main__":
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

    app = RecorderApplication()
    app.exec_()

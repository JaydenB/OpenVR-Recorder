import ui.recorder_widget as rw

from PyQt5 import QtWidgets, QtCore, QtGui


class TrackedDevice(object):
    def __init__(self, _parent, _vr_tracked_device):
        self.parent = _parent

        self.name = _vr_tracked_device
        self.serial_number = 0

        self.table_widget = rw.TrackedDeviceWidget(_vr_tracked_device)
        self.row = self.parent.ui_widget.add_device(self.table_widget)

    def update_pose(self, sample):
        """Updates the Device's pose in Euler in the display table"""
        for column in range(0, 6):
            display_value = round(sample[column], 4)
            self.parent.ui_widget.tb_devices.setItem(
                self.row, column + 2,
                QtWidgets.QTableWidgetItem(str(display_value)))

import ui.recorder_widget


class TrackedDevice(object):
    def __init__(self, _parent, _vr_tracked_device):
        self.parent = _parent

        self.name = ""
        self.serial_number = 0

        self.table_widget = ui.recorder_widget.TrackedDeviceWidget()
        self.parent.ui.add_device(self.table_widget)

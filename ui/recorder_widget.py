from PyQt5 import QtWidgets, QtCore, QtGui
from .viewport_widget import ViewportWidget


DEFAULT_FILEPATH = "C:/recordings/steamvr"


class RecorderWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.resize(850, 600)

        # -----------------------------------------
        #   Connection
        # -----------------------------------------

        layout_connection = QtWidgets.QHBoxLayout()

        self.pb_calibrate = QtWidgets.QPushButton("CALIB")
        self.pb_record = QtWidgets.QPushButton()
        self.pb_connection = QtWidgets.QPushButton()

        self.update_record_icon(False)
        self.pb_record.setIconSize(QtCore.QSize(40, 40))
        self.update_connected_icon(False)
        self.pb_connection.setIconSize(QtCore.QSize(40, 40))

        # Stylesheets
        self.pb_calibrate.setStyleSheet("""QPushButton:pressed {
                            background-color: rgb(180, 180, 180);
                        }""")
        self.pb_record.setStyleSheet("""QPushButton:pressed {
                    background-color: rgb(180, 180, 180);
                }""")
        self.pb_connection.setStyleSheet("""QPushButton:pressed {
                    background-color: rgb(180, 180, 180);
                }""")

        self.pb_calibrate.setFixedSize(50, 50)
        self.pb_record.setFixedSize(50, 50)
        self.pb_connection.setFixedSize(50, 50)

        layout_connection.addWidget(self.pb_calibrate)
        layout_connection.addWidget(self.pb_connection)
        layout_connection.addWidget(self.pb_record)

        # -----------------------------------------
        #   Recording Settings
        # -----------------------------------------

        layout_recording_settings = QtWidgets.QHBoxLayout()

        spacer_01_recording_settings = QtWidgets.QSpacerItem(40, 20,
                                                             QtWidgets.QSizePolicy.Expanding,
                                                             QtWidgets.QSizePolicy.Minimum)

        lbl_slate = QtWidgets.QLabel("Slate:")
        self.le_slate = QtWidgets.QLineEdit("default")
        lbl_setup = QtWidgets.QLabel("Setup:")
        self.le_setup = QtWidgets.QLineEdit("default")
        lbl_take = QtWidgets.QLabel("Take:")
        self.sb_take = QtWidgets.QSpinBox()

        self.le_slate.setFixedWidth(100)
        self.le_setup.setFixedWidth(100)
        self.sb_take.setFixedWidth(50)

        self.sb_take.setMinimum(1)

        layout_recording_settings.addWidget(lbl_slate)
        layout_recording_settings.addWidget(self.le_slate)
        layout_recording_settings.addWidget(lbl_setup)
        layout_recording_settings.addWidget(self.le_setup)
        layout_recording_settings.addWidget(lbl_take)
        layout_recording_settings.addWidget(self.sb_take)
        layout_recording_settings.addItem(spacer_01_recording_settings)

        # -----------------------------------------
        #   Others
        # -----------------------------------------

        layout_other = QtWidgets.QVBoxLayout()

        self.lbl_status = QtWidgets.QLabel("Idle.")
        self.file_browser = FileBrowserWidget()

        self.lbl_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        layout_other.addWidget(self.lbl_status)
        layout_other.addWidget(self.file_browser)

        # -----------------------------------------
        #   Live Devices Table
        # -----------------------------------------

        layout_devices = QtWidgets.QHBoxLayout()

        self.tb_devices = QtWidgets.QTableWidget()

        columns = ["Device", "Serial", "t.x", "t.y", "t.z", "r.x", "r.y", "r.z"]
        for index, column in enumerate(columns):
            self.tb_devices.insertColumn(index)
            self.tb_devices.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(column))

        layout_devices.addWidget(self.tb_devices)

        # -----------------------------------------
        #   Live 3D Viewport
        # -----------------------------------------

        # widget_viewport = QtWidgets.QWidget()
        # layout_viewport = QtWidgets.QVBoxLayout()

        self.viewport = ViewportWidget()

        # layout_viewport.addWidget(self.viewport)
        # widget_viewport.setLayout(layout_viewport)

        # -----------------------------------------
        #   Collate everything together with a QSplitter...
        # -----------------------------------------

        splitter_layout_top = QtWidgets.QVBoxLayout()
        splitter_widget_top = QtWidgets.QWidget()

        layout_top = QtWidgets.QHBoxLayout()
        layout_top.addLayout(layout_other)
        layout_top.addLayout(layout_connection)

        splitter_layout_top.addLayout(layout_top)
        splitter_layout_top.addLayout(layout_recording_settings)
        splitter_layout_top.addLayout(layout_devices)
        splitter_widget_top.setLayout(splitter_layout_top)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical, self)
        splitter.addWidget(splitter_widget_top)
        splitter.addWidget(self.viewport)

        self.main_layout.addWidget(splitter)

    def update_record_icon(self, state):
        if state:
            self.pb_record.setIcon(QtGui.QIcon("./ui/icons/icon_record_stop.png"))
        else:
            self.pb_record.setIcon(QtGui.QIcon("./ui/icons/icon_record_start.png"))

    def update_connected_icon(self, state):
        if state:
            self.pb_connection.setIcon(QtGui.QIcon("./ui/icons/icon_connected.png"))
        else:
            self.pb_connection.setIcon(QtGui.QIcon("./ui/icons/icon_disconnected.png"))

    def add_device(self, device):
        print("Adding '%s' to table_widget for devices!" % device)
        # new_row =  + 1
        self.tb_devices.insertRow(self.tb_devices.rowCount())
        # print("newRow: %s" % new_row)
        self.tb_devices.setItem(self.tb_devices.rowCount()-1, 0, device)
        print("device inserted.")
        return self.tb_devices.rowCount()-1

    def clear_devices(self):
        # @TODO: Loop through all Table Widget items within self.tb_devices and remove
        self.tb_devices.setRowCount(0)


class TrackedDeviceWidget(QtWidgets.QTableWidgetItem):
    def __init__(self, name):
        QtWidgets.QTableWidgetItem.__init__(self, name)


class FileBrowserWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.pb_browse = QtWidgets.QPushButton()
        self.le_filepath = QtWidgets.QLineEdit(DEFAULT_FILEPATH)

        self.pb_browse.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirIcon))
        self.le_filepath.setReadOnly(True)

        self.main_layout.addWidget(self.pb_browse)
        self.main_layout.addWidget(self.le_filepath)

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- SIGNALS ----------
        self.pb_browse.clicked.connect(self.clicked_browse)

    def clicked_browse(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDirectory("C:/")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.DirectoryOnly)
        if file_dialog.exec_():
            self.selected_folder(file_dialog.selectedFiles())

    def selected_folder(self, selected_files):
        self.le_filepath.setText(selected_files[0])

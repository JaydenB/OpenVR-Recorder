from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import Qt3DCore, Qt3DRender, Qt3DExtras


class ViewportWidget(QtWidgets.QWidget):
    start_playback = QtCore.pyqtSignal()
    stop_playback = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.hand_control = True

        main_layout = QtWidgets.QVBoxLayout()

        # Build 3D Viewport
        self.window = ViewportWindow(self)
        self.create_scene()

        # fov slider
        self.slider_fov = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider_fov.setMinimum(1)
        self.slider_fov.setMaximum(120)
        self.slider_fov.setValue(60)
        main_layout.addWidget(self.slider_fov)
        self.slider_fov.valueChanged.connect(self.adjust_fov)

        self.window_widget = QtWidgets.QWidget.createWindowContainer(self.window, self)
        main_layout.addWidget(self.window_widget)

        self.setLayout(main_layout)

    def create_scene(self):
        # ----- Root Entity for the SceneGraph -----
        self.entity_root = Qt3DCore.QEntity()

        # ----- Create Camera Representation -----
        self.entity_cube = Qt3DCore.QEntity(self.entity_root)
        mesh_cube = Qt3DExtras.QCuboidMesh()
        mesh_import = Qt3DRender.QMesh()
        mesh_import.setSource(QtCore.QUrl.fromLocalFile("./ui/meshes/mmcube.obj"))

        self.transform_cube = Qt3DCore.QTransform()
        self.transform_cube.setScale(10.0)       # scale to be larger than camera
        self.transform_cube.setRotationY(-90)   # make sure we face towards center face

        # Textured Material for Cube
        loader = Qt3DRender.QTextureLoader(self.entity_cube)
        material = Qt3DExtras.QTextureMaterial(self.entity_cube)
        loader.setSource(QtCore.QUrl.fromLocalFile("./ui/meshes/mmcube_diff.png"))
        material.setTexture(loader)

        self.entity_cube.addComponent(mesh_import)
        self.entity_cube.addComponent(self.transform_cube)
        self.entity_cube.addComponent(material)

        # ----- Create Camera -----
        self.camera = self.window.camera()
        self.camera.lens().setPerspectiveProjection(60.0,
                                                    16.0 / 9.0,
                                                    0.1, 1000.0)
        self.camera.setPosition(QtGui.QVector3D(0.0, 0.0, 0.0))

        # ----- Set Root Entity -----
        self.window.setRootEntity(self.entity_root)

    def move_camera(self, diff_x, diff_y):
        if not self.hand_control:
            return

        mult = 0.2
        self.camera.tilt(-diff_y*mult)
        self.camera.pan(diff_x*mult)

    def adjust_fov(self, new_value):
        # self.camera.lens().setPerspectiveProjection(float(new_value),
        #                                             16.0 / 9.0,
        #                                             0.1, 1000.0)
        self.camera.setFieldOfView(float(new_value))

    def update_camera_with_sample(self, sample):
        # @TODO: You know what to do here.
        #   Shouldn't take too long but also not 100% necessary right now

        p = sample['tracker_1']['position']
        q = sample['tracker_1']['quaternion']
        self.camera.transform().setRotation(QtGui.QQuaternion(q[0], q[1],
                                                              q[2], q[3]))
        scale = 1
        self.camera.transform().setTranslation(QtGui.QVector3D(p[0]*scale, p[1]*scale, p[2]*scale))


class ViewportWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self, parent=None):
        Qt3DExtras.Qt3DWindow.__init__(self, None)
        self.parent = parent

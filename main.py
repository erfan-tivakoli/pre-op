import math

from PyQt5.QtGui import QPen, QPainter, QPainterPath
from PyQt5.QtWidgets import QMessageBox, QDial, QGraphicsItem, QComboBox, QSlider, QFileDialog, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRectF

from coin_detector import find_coin

lldButton_clicked = False


class MouseTracker(QWidget):

    def __init__(self, viewer):
        super().__init__()
        self.initUI()
        self.viewer = viewer

    def initUI(self):
        # self.setGeometry(0, 0, 1000, 1000)
        # self.setWindowTitle('Mouse Tracker')
        # self.label = QLabel(self)
        # self.label.resize(500, 40)

        self.setMouseTracking(True)
        self.setStyleSheet("background-color: rgba(0,0,0,0)")

        self.show()
        self.pos = None
        self.positions = []
        self.installEventFilter(self)


    def mouseMoveEvent(self, event):
        QtWidgets.QApplication.sendEvent(self.viewer, event)
        print('moving in tracker')
        if 0 < len(self.positions) < 4:
            self.pos = event.pos()
            self.update()
        else:
            pass

    def mousePressEvent(self, QMouseEvent):
        QtWidgets.QApplication.sendEvent(self.viewer, QMouseEvent)
        print('first')
        global lldButton_clicked
        if not lldButton_clicked:
            return
        if len(self.positions) == 4:
            self.positions = [QMouseEvent.pos()]
        elif len(self.positions) < 4:
            self.positions.append(QMouseEvent.pos())

    def paintEvent(self, event):
        if self.pos and len(self.positions) > 0:
            q = QPainter(self)
            pen = QPen(QtCore.Qt.green, 5)
            q.setPen(pen)
            for i in range(len(self.positions) - 1):
                q.drawLine(self.positions[i].x(), self.positions[i].y(), self.positions[i + 1].x(),
                           self.positions[i + 1].y())
            q.drawLine(self.positions[-1].x(), self.positions[-1].y(), self.pos.x(), self.pos.y())

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.positions = []
            self.update()


class MovableImage(QtWidgets.QGraphicsPixmapItem):
    """Provide a movable image"""

    def __init__(self):
        super().__init__()  # Initial position must be (0,0) to avoid bias in coordinate system...
        self.setPixmap(QtGui.QPixmap())
        self.setAcceptHoverEvents(True)  # hover events are used to change mouse cursor
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setOpacity(0.1)

    def setNewPixmap(self, pixmap):
        self.setPixmap(pixmap)


class ShellItem(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(250, 250)
        self.clicked_in_rotation_area = False

    def boundingRect(self):
        return QRectF(180, 180, 140, 90)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.red)

        painter.drawPie(200, 200, 100, 100, 0, 180 * 16)

        painter.drawPie(210, 210, 80, 80, 0, 180 * 16)

        painter.drawPie(180, 180, 140, 140, 0, 180 * 16)

        pen = QPen(QtCore.Qt.green, 3, QtCore.Qt.DashDotLine)
        painter.setPen(pen)
        painter.drawLine(250, 270, 250, 180)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        print('stem press')
        x = QGraphicsSceneMouseEvent.scenePos().x() - self.pos().x() - self.transformOriginPoint().x()
        y = QGraphicsSceneMouseEvent.scenePos().y() - self.pos().y() - self.transformOriginPoint().y()
        self.first_rotation = math.atan2(y, x) * 180 / math.pi - self.rotation()

        if 2500 < x * x + y * y < 4900:
            self.clicked_in_rotation_area = True
        else:
            self.clicked_in_rotation_area = False

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        super().mouseReleaseEvent(QGraphicsSceneMouseEvent)
        self.clicked_in_rotation_area = False

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        print('stem moving')
        x = QGraphicsSceneMouseEvent.scenePos().x() - self.pos().x() - self.transformOriginPoint().x()
        y = QGraphicsSceneMouseEvent.scenePos().y() - self.pos().y() - self.transformOriginPoint().y()

        if self.clicked_in_rotation_area:
            self.setRotation(math.atan2(y, x) * 180 / math.pi - self.first_rotation)
        else:
            super().mouseMoveEvent(QGraphicsSceneMouseEvent)
        self.update()

    def shape(self):
        mypath = QPainterPath()
        mypath.arcTo(180,180, 140, 140,0, 360)
        mypath.closeSubpath()
        return mypath


class StemItem(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setOpacity(0.2)

    def boundingRect(self):
        return QRectF(0, 78, 155, 425)

    def paint(self, painter, option, widget=None):
        pen = QPen(QtCore.Qt.blue, 5)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.blue)

        polygon = QtGui.QPolygonF()
        polygon.append(QtCore.QPointF(114, 80))
        polygon.append(QtCore.QPointF(94, 113))
        polygon.append(QtCore.QPointF(91, 120))
        polygon.append(QtCore.QPointF(53, 166))
        polygon.append(QtCore.QPointF(3, 176))
        polygon.append(QtCore.QPointF(13, 317))
        polygon.append(QtCore.QPointF(86, 502))
        polygon.append(QtCore.QPointF(101, 499))
        polygon.append(QtCore.QPointF(73, 317))
        polygon.append(QtCore.QPointF(106, 196))
        polygon.append(QtCore.QPointF(124, 136))
        polygon.append(QtCore.QPointF(129, 136))
        polygon.append(QtCore.QPointF(147, 100))

        painter.drawPolygon(polygon)


    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        print('femeral moving')
        super().mouseMoveEvent(QGraphicsSceneMouseEvent)
        self.update()

    def shape(self):
        myPath = QPainterPath()
        polygon = QtGui.QPolygonF()
        polygon.append(QtCore.QPointF(114, 80))
        polygon.append(QtCore.QPointF(94, 113))
        polygon.append(QtCore.QPointF(91, 120))
        polygon.append(QtCore.QPointF(53, 166))
        polygon.append(QtCore.QPointF(3, 176))
        polygon.append(QtCore.QPointF(13, 317))
        polygon.append(QtCore.QPointF(86, 502))
        polygon.append(QtCore.QPointF(101, 499))
        polygon.append(QtCore.QPointF(73, 317))
        polygon.append(QtCore.QPointF(106, 196))
        polygon.append(QtCore.QPointF(124, 136))
        polygon.append(QtCore.QPointF(129, 136))
        polygon.append(QtCore.QPointF(147, 100))
        myPath.addPolygon(polygon)
        return myPath


class PhotoViewer(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self.lld = MouseTracker(self)
        # self.small_part = MovableImage()
        # self.big_part = MovableImage()
        self.small_part = ShellItem()
        self.big_part = StemItem()

        self._scene.addItem(self._photo)
        # self._scene.addItem(self.big_part)
        # self._scene.addItem(self.small_part)
        self._scene.addWidget(self.lld)

        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.vertices = []

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):

        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.lld.setGeometry(0, 0, pixmap.width(), pixmap.height())


        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)

        # Combo for shell selecting
        self.shellCombo = QtWidgets.QComboBox(self)
        self.shellCombo.addItem('Select Shell type')
        self.shellCombo.addItem('Type 1')
        self.shellCombo.addItem('Type 2')
        self.shellCombo.currentIndexChanged.connect(self.loadShell)
        self.shellCombo.hide()

        # Combo for stem selecting
        self.stemCombo = QtWidgets.QComboBox(self)
        self.stemCombo.addItem('Select Stem type')
        self.stemCombo.addItem('Type 1')
        self.stemCombo.addItem('Type 2')
        self.stemCombo.currentIndexChanged.connect(self.loadStem)
        self.stemCombo.hide()



        # QSlider for size change
        self.mySlider = QSlider(Qt.Horizontal, self)
        self.mySlider.setMinimum(50)
        self.mySlider.setMaximum(300)
        self.mySlider.setSliderPosition(100)
        self.mySlider.valueChanged[int].connect(self.changeValue)
        self.mySlider.hide()

        # Push button for calibration
        self.calibratebtn = QtWidgets.QToolButton(self)
        self.calibratebtn.setText('Calibrate')
        self.calibratebtn.clicked.connect(self.calibrate)
        self.calibratebtn.hide()

        # Push button for lld
        self.lldButton = QtWidgets.QPushButton(self)
        self.lldButton.setText('lld')
        self.lldButton.setCheckable(True)
        self.lldButton.clicked.connect(self.lldButton_click_handler)
        self.lldButton.hide()

        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.shellCombo)
        HBlayout.addWidget(self.stemCombo)
        HBlayout.addWidget(self.lldButton)

        HBlayout.addWidget(self.calibratebtn)
        HBlayout.addWidget(self.mySlider)
        VBlayout.addLayout(HBlayout)

    def loadImage(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                         'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if self.image_path:
            self.viewer.setPhoto(QtGui.QPixmap(self.image_path))
            self.shellCombo.show()
        else:
            pass

    def loadShell(self):
        if 'Type' not in self.shellCombo.currentText():
            return
        self.viewer._scene.addItem(self.viewer.small_part)
        self.stemCombo.show()

    def loadStem(self):
        if 'Type' not in self.stemCombo.currentText():
            return
        self.viewer._scene.addItem(self.viewer.big_part)
        self.calibratebtn.show()

    # def operate(self):
    #     if self.viewer.hasPhoto():
    #         self.viewer.small_part.setNewPixmap(QtGui.QPixmap('images/hamed_small.jpg'))
    #         self.viewer.big_part.setNewPixmap(QtGui.QPixmap('images/hamed_big.jpg'))
    #     else:
    #         msg = QMessageBox()
    #         msg.setIcon(QMessageBox.Information)
    #
    #         msg.setText("Error")
    #         msg.setInformativeText("You should load an image before operation")
    #         msg.setWindowTitle("No Image")
    #         msg.setStandardButtons(QMessageBox.Ok)
    #
    #         msg.exec_()

    def sliderMoved(self):
        x = self.viewer.small_part.boundingRect().center().x()
        y = self.viewer.small_part.boundingRect().center().y()
        self.viewer.small_part.setTransformOriginPoint(y, x)
        self.viewer.small_part.setRotation(self.dial.value())


    def changeValue(self, value):
        if self.viewer.small_part.isSelected():
            self.viewer.small_part.setScale(float(value / 100))
        elif self.viewer.big_part.isSelected():
            self.viewer.big_part.setScale(float(value / 100))

    def calibrate(self):
        new_path = find_coin(self.image_path)
        self.viewer.setPhoto(QtGui.QPixmap(new_path))
        self.image_path = new_path
        self.lldButton.show()

    def lldButton_click_handler(self):
        global lldButton_clicked

        if lldButton_clicked:
            lldButton_clicked = False
        else:
            lldButton_clicked = True


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())

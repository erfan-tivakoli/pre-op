from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsEllipseItem, \
    QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QMessageBox
from PyQt5.QtCore import Qt, QPointF


class MovableImage(QtWidgets.QGraphicsPixmapItem):
    """Provide a movable image"""

    def __init__(self, image_address):
        super().__init__()  # Initial position must be (0,0) to avoid bias in coordinate system...
        # self.setPixmap(QtGui.QPixmap(image_address))
        self.setPixmap(QtGui.QPixmap())
        self.setAcceptHoverEvents(True)  # hover events are used to change mouse cursor

    def setNewPixmap(self, pixmap):
        self.setPixmap(pixmap)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor enters the object, set cursor to open hand"""
        QApplication.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor leaves the object, restore mouse cursor"""
        QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """mouseMoveEvent is called whenever a mouse button is pressed and the cursor is moved. """
        new_cursor_position = event.scenePos()  # mouse cursor in scene coordinates
        old_cursor_position = event.lastScenePos()
        old_top_left_corner = self.scenePos()
        new_top_left_corner_x = new_cursor_position.x() - old_cursor_position.x() + old_top_left_corner.x()
        new_top_left_corner_y = new_cursor_position.y() - old_cursor_position.y() + old_top_left_corner.y()
        self.setPos(QPointF(new_top_left_corner_x, new_top_left_corner_y))  # update disk top left corner

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'): pass


class PhotoViewer(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setTransformationMode(Qt.SmoothTransformation)
        self._photo.setTransformOriginPoint()
        self.small_part = MovableImage('images/small_part.png')
        self.small_part.setTransformationMode(Qt.SmoothTransformation)
        self.big_part = MovableImage('images/big_part.png')

        self._scene.addItem(self._photo)
        self._scene.addItem(self.big_part)
        self._scene.addItem(self.small_part)

        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

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
        # pixmap2 = QtGui.QPixmap('t.png')
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            # self._photo2.setPixmap(pixmap2)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
            # self._photo2.setPixmap(QtGui.QPixmap())
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
        # Button to change from drag/pan to getting pixel info
        self.btnOperate = QtWidgets.QToolButton(self)
        self.btnOperate.setText('Operate')
        self.btnOperate.clicked.connect(self.operate)

        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnOperate)
        VBlayout.addLayout(HBlayout)

    def loadImage(self):
        self.viewer.setPhoto(QtGui.QPixmap('images/hip.jpg'))

    def operate(self):
        if self.viewer.hasPhoto():
            self.viewer.small_part.setNewPixmap(QtGui.QPixmap('images/small_part.png'))
            self.viewer.big_part.setNewPixmap(QtGui.QPixmap('images/big_part.png'))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Error")
            msg.setInformativeText("You should load an image before operation")
            msg.setWindowTitle("No Image")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()




if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())

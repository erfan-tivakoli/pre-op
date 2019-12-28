from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPolygon, QPen

# class RectItem(QtWidgets.QGraphicsRectItem):
#     def paint(self, painter, option, widget=None):
#         super(RectItem, self).paint(painter, option, widget)
#         painter.save()
#
#         painter.setRenderHint(QtGui.QPainter.Antialiasing)
#         painter.setBrush(QtCore.Qt.red)
#         painter.drawEllipse(option.rect)
#         # painter.setOpacity(0.1)
#
#         painter.restore()
from PyQt5.QtWidgets import QGraphicsEllipseItem


class StemItem(QtWidgets.QGraphicsItem):
    def boundingRect(self):
        return QRectF(200, 200, 100, 100)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.red)
        # painter.drawEllipse(200, 200, 100, 100)
        painter.drawPie(200, 200, 100, 100, 0, 180 * 16)

        painter.drawPie(210, 210, 80, 80, 0, 180 * 16)

        pen = QPen(QtCore.Qt.green, 3, QtCore.Qt.DashDotLine)
        painter.setPen(pen)
        painter.drawLine(250, 270, 250, 180)


class FemeralItem(QtWidgets.QGraphicsItem):
    def boundingRect(self):
        return QRectF(0, 0, 150, 500)

    def paint(self, painter, option, widget=None):
        pen = QPen(QtCore.Qt.blue, 5)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.blue)

        # painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.setBrush(QtCore.Qt.blue)

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

        # for i in range(10):
        #     polygon.append(QtCore.QPointF(i* 100, i* 100))
        painter.drawPolygon(polygon)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        view = QtWidgets.QGraphicsView(scene)
        self.setCentralWidget(view)

        pixmap = QtGui.QPixmap("../images/hip.jpg")
        photo = QtWidgets.QGraphicsPixmapItem()
        photo.setPixmap(pixmap)
        scene.addItem(photo)

        # rect_item = StemItem()
        rect_item = FemeralItem()
        rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # rect_item.setTransformOriginPoint(250, 250)
        rect_item.setRotation(0)
        rect_item.setOpacity(0.2)
        rect_item.setScale(0.5)

        scene.addItem(rect_item)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())

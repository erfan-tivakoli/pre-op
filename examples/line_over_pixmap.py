import sys

from PyQt5.QtWidgets import QMessageBox, QDial, QGraphicsItem, QComboBox, QSlider
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 500, 300)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("../images/hip.jpg")

        painter.drawPixmap(self.rect(), pixmap)
        pen = QtGui.QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() - 10, 10)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

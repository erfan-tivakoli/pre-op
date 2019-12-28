import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen



class MouseTracker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()
        self.pos = None
        self.positions = []

    def mouseMoveEvent(self, event):
        if 0 < len(self.positions) < 4:
            self.pos = event.pos()
            self.update()
        else:
            pass

    def mousePressEvent(self, QMouseEvent):
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


app = QApplication(sys.argv)
ex = MouseTracker()

sys.exit(app.exec_())

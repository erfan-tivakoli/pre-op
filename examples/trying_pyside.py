import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QWidget, QLabel, QApplication


class MouseTracker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()
        self.pos = None
        self.positions = []

        self.installEventFilter(self)


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
            pen = QPen(Qt.green, 5)
            q.setPen(pen)
            for i in range(len(self.positions) - 1):
                q.drawLine(self.positions[i].x(), self.positions[i].y(), self.positions[i + 1].x(),
                           self.positions[i + 1].y())
            q.drawLine(self.positions[-1].x(), self.positions[-1].y(), self.pos.x(), self.pos.y())


    def eventFilter(self, object, event):
        return True

app = QApplication(sys.argv)
ex = MouseTracker()

sys.exit(app.exec_())

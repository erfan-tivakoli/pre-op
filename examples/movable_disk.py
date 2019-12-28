import sys
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsEllipseItem, \
    QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class MovableDisk(QtWidgets.QGraphicsPixmapItem):
    """Provide a movable red disk w/o using itemIsMovable flag"""
    def __init__(self):
        super().__init__()  # Initial position must be (0,0) to avoid bias in coordinate system...
        self.setPixmap(QtGui.QPixmap('images/small_part.png'))
        self.setAcceptHoverEvents(True)  # hover events are used to change mouse cursor

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


class MyView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 2500, 2500)
        self.disk = MovableDisk()
        self.scene.addItem(self.disk)


if __name__ == '__main__':
    app = QApplication([])
    f = MyView()
    f.show()
    sys.exit(app.exec_())

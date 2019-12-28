import sys
from PyQt5 import QtCore, QtWidgets
from view_cortes2 import Ui_cortes2

class MainWindow(QtWidgets.QMainWindow, Ui_cortes2):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.flag = 0
        self.ledit_corteA.installEventFilter(self)
        self.ledit_corteB.installEventFilter(self)
        #self.buttonGroup.buttonClicked.connect(self.handleButtons)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.FocusIn and source is self.ledit_corteA:
            print("A")
            self.flag = 0
        if event.type() == QtCore.QEvent.FocusIn and source is self.ledit_corteB:
            print("B")
            self.flag = 1
        return super(MainWindow, self).eventFilter(source, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

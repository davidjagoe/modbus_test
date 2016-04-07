
import os

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt
import PyQt4.uic as uic


def load_ui(window):
    f = os.path.join(os.path.dirname(__file__), "layout", "main_window.ui")
    uic.loadUi(f, window)

    
class MainWindow(qt.QMainWindow):

    BLACK = "QLCDNumber{color:rgb(0, 0, 0);}"
    RED = "QLCDNumber{color:rgb(255, 0, 0);}"

    def __init__(self, application):
        qt.QMainWindow.__init__(self)
        load_ui(self)
        self._application = application
        self._setup()

    def _setup(self):
        # self.rpmDisplay.setSegmentStyle(qt.QLCDNumber.Flat)
        self.alarmLabel.setText("")
        self._application.listen(self._update_value)
        
    def closeEvent(self, *args):
        qt.QMainWindow.closeEvent(self, *args)
        
    def _update_value(self, value):
        self.rpmDisplay.display(value)
        if value <= 10:
            self.alarmLabel.setText("LOW")
            self.rpmDisplay.setStyleSheet(self.RED)
        else:
            self.alarmLabel.setText("")
            self.rpmDisplay.setStyleSheet(self.BLACK)
        

### Public Interface

def get_main_window(application):
    return MainWindow(application)

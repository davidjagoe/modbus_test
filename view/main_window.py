
import os

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt
import PyQt4.uic as uic


def load_ui(window):
    f = os.path.join(os.path.dirname(__file__), "layout", "main_window.ui")
    uic.loadUi(f, window)

    
class MainWindow(qt.QMainWindow):

    BLACK = "QLabel {color:rgb(0, 0, 0);}"
    AMBER = "QLabel {color:rgb(255, 255, 0);}"
    RED = "QLabel {color:rgb(255, 0, 0);}"

    def __init__(self, application):
        qt.QMainWindow.__init__(self)
        load_ui(self)
        self._application = application
        self._setup()

    def _setup(self):
        self.rpmLabel.setText("LOW")
        self._application.listen(self._update_value)
    
    def closeEvent(self, *args):
        qt.QMainWindow.closeEvent(self, *args)
    
    def _update_value(self, value):
        print value
        self.rpmLabel.setText(str(value))
        if value < 5:
            self.rpmLabel.setText("STALL")
            self.rpmLabel.setStyleSheet(self.RED)
        elif value < 10:
            self.rpmLabel.setText("LOW")
            self.rpmLabel.setStyleSheet(self.AMBER)
        elif value <= 20:
            self.rpmLabel.setText("OK")
            self.rpmLabel.setStyleSheet(self.BLACK)
        else:
            self.rpmLabel.setText("HIGH")
            self.rpmLabel.setStyleSheet(self.RED)
        

### Public Interface

def get_main_window(application):
    return MainWindow(application)

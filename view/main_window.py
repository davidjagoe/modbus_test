
import os

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt
import PyQt4.uic as uic


def load_ui(window):
    f = os.path.join(os.path.dirname(__file__), "layout", "main_window.ui")
    uic.loadUi(f, window)

    
class MainWindow(qt.QMainWindow):

    def __init__(self):
        qt.QMainWindow.__init__(self)
        load_ui(self)

    def closeEvent(self, *args):
        qt.QMainWindow.closeEvent(self, *args)
        
    def _layout(self):
        pass

    def _close(self):
        self.close()


### Public Interface

def get_main_window():
    return MainWindow()
